#!/usr/bin/env python

import xmltodict
import json
import sys
from device import Device

def doshow(dev, cmd):
    try:
       results_xml = dev.show(cmd)
    except:
       return {}
    results_dict = xmltodict.parse(results_xml[1])
    return results_dict['ins_api']['outputs']['output']['body']

def displaydictionary(dict):
    results_asc = json.dumps(dict, indent=4)
    print results_asc

# ----------------------------------------------------------
# getmac is passed an open Device object
# it returns a dictionary of:
#
#   dict[mac]['interface'] = interface
#   dict[mac]['vlan'] = vlan
#
# Author: Beau Poehls!

def getmac(device):
    '''
    Function to make call to nxapi for a switch's mac-address table.
    '''
    show_mac_dict = doshow(device,'show mac address dynamic')
    data = show_mac_dict['TABLE_mac_address']['ROW_mac_address']
    clean_dict={}
    for x in range(len(data)):
        mac_dict = data[x]
        clean_dict[mac_dict['disp_mac_addr']] = {
            "interface":mac_dict['disp_port'],
            "vlan":mac_dict['disp_vlan'],
        }
    return clean_dict

# ----------------------------------------------------------
# getarp is passed an open Device object
# it returns a dictionary of:
#
#   dict[mac]['iplist'][ip][interface] = count
#
# Author: Jeremy Guthrie!

def getarp(dev):
    sh_arp_dict = doshow(dev,'show ip arp vrf all')
    data = sh_arp_dict['TABLE_vrf']['ROW_vrf']['TABLE_adj']['ROW_adj']
    clean_dict={}
    for loop in range(len(data)):
        arp_dict=data[loop]
        mac = arp_dict['mac']
        ipaddr= arp_dict['ip-addr-out']
        intf = arp_dict['intf-out']
        if not mac in clean_dict:
           clean_dict[mac] = { "iplist": { data[loop]['ip-addr-out']: { data[loop]['intf-out']: 1 } } }
        else:
           clean_dict[mac]['iplist'][ipaddr]={ intf:1 }
    return clean_dict

# ----------------------------------------------------------
def getsysname(dev):
    return doshow(dev,'show hostname')

# ----------------------------------------------------------
# getneighbors is passed a seed IP, username, password
# it returns a list of IP addresses (including the original one passed)
#
# Author: Jeremy Guthrie!

def show_cdwneighbors(dev,devices):
    sh_cdpneighbors_list = doshow(dev,'show cdp neighbors detail')
    cdpneighbors_list = []
    if sh_cdpneighbors_list:
       data = sh_cdpneighbors_list['TABLE_cdp_neighbor_detail_info']['ROW_cdp_neighbor_detail_info']
       platform=""
       for loop in range(len(data)):
           for key,value in data[loop].iteritems():
               if key == "v4mgmtaddr":
                   if not value in devices:
                       cdpneighbors_list.append(value)
                       ipaddr = value
    return cdpneighbors_list

def getneighbors(ip,username,password):
    devices = [ ip ]
    devicecount=0
    while devicecount != len(devices):
        dev = Device(ip=devices[devicecount], username=username, password=password)
        dev.open()
        devices = devices + show_cdwneighbors(dev,devices)
        devicecount+=1
    return devices

# ----------------------------------------------------------
# portmap takes all the data and munches it into a report

def portmap(results):
   switches = results.keys()

   # first pass, count the number of MACs on each swport (switch + interface)
   interface_mac_count={}
   for switch in switches:
      for mac in results[switch]['mac']:
         interface = results[switch]['mac'][mac]['interface']
         swport = switch + ',' + interface
         if not swport in interface_mac_count:
            interface_mac_count[swport] = 0
         interface_mac_count[swport] += 1

   # second pass, find the "home" swport for each MAC (the swport with the fewest total MACs)
   all_macs={}
   all_mac_count={}
   for switch in switches:
      for mac in results[switch]['mac']:
         interface = results[switch]['mac'][mac]['interface']
         swport = switch + ',' + interface

         # MAC is new, store as-is to all_macs
         if not mac in all_macs:
            all_mac_count[mac]=interface_mac_count[swport]
            all_macs[mac]={
                'ports':[ swport ],
                'ip(s)':'',
            }

         # MAC is on a better port, update the all_macs
         elif interface_mac_count[swport] < all_mac_count[mac]:
            all_mac_count[mac] = interface_mac_count[swport]
            all_macs[mac]['ports'] = [ swport ]

         # MAC is on a port of equal weight, append it to the existing list
         elif interface_mac_count[swport] == all_mac_count[mac]:
            all_macs[mac]['ports'].append(swport)

   # third pass, try to stitch in IP address info from the ARP table
   all_ips={}
   for switch in switches:
      for mac in results[switch]['arp']:
         iplist = results[switch]['arp'][mac]['iplist']
         ipaddrs = []
         for ipaddr in iplist.keys():
            ipaddrs.append(ipaddr)
         if mac in all_macs:
            all_macs[mac]['ip(s)'] = ",".join(ipaddrs)
         # silently discard ARP entries for which we have no L2 info

   displaydictionary(all_macs)
   displaydictionary(nicenames)
   return

# ----------------------------------------------------------
# main code

if __name__ == "__main__":

    args=sys.argv
    if len(args) < 4:
        print "usage: portmap.py <username> <password> <ip [ip ..]>"
        exit(1);

    username = args[1]
    password = args[2]
    ipaddrs = {}

    for seedip in args[3:]:
       if not seedip in ipaddrs:
           for ip in getneighbors(seedip, username, password):
              ipaddrs[ip] = 1

    results = {}
    nicenames={}

    for ipaddr in ipaddrs.iterkeys():
       dev = Device(ip=ipaddr, password=password, username=username)
       dev.open()
       if doshow(dev,'show clock'):
          print 'checking: ' + ipaddr
          results[ipaddr] = {}
          results[ipaddr]['mac']=getmac(dev)
          results[ipaddr]['arp']=getarp(dev)
          nicenames[ipaddr]=getsysname(dev)
       else:
         print "failed: " + ipaddr

    portmap(results)
