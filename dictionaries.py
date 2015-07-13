print "1.1.2 - START"
router1 = {'os_version':'3.1.1', 'hostname':'nyc_router1', 'model':'nexus 9396', 'domain':'cisco.com', 'mgmt_ip':'10.1.50.11'}
router2 = dict( os_version='3.2.1', hostname='rtp_router2', model='nexus 9396', domain='cisco.com', mgmt_ip='10.1.50.12')

os_version = '3.1.1'
hostname = 'ROUTER3'
model = 'nexus 9396'
domain = 'lab.cisco.com'
mgmt_ip = '10.1.50.13'
router3 = {'os_version':os_version,'hostname': hostname,'model':model,'domain':domain,'mgmt_ip':mgmt_ip}

print router1['hostname']
print router1['os_version']

print router3['hostname']

router2['os_version'] = '3.1.1'
print router2['os_version']

router3['model'] = 'nexus 9504'
print router3['model']

print router3.keys()

router2.has_key('hostname')


def getRouter(rtr):
    router1 = {'os_version':'3.1.1', 'hostname':'nyc_router1', 'model':'nexus 9396', 'domain':'cisco.com', 'mgmt_ip':'10.1.50.11'}
    router2 = dict( os_version='3.2.1', hostname='rtp_router2', model='nexus 9396', domain='cisco.com', mgmt_ip='10.1.50.12')
    router3 = dict( os_version='3.1.1', hostname='ROUTER3', model='nexus 9504', domain='lab.cisco.com', mgmt_ip='10.1.50.13')
    if rtr == 'router1':
        return router1
    elif rtr == 'router2':
        return router2
    elif rtr == 'router2':
        return router3
    return 'No router found.'

result1 = getRouter('router1')
print "router1:  "
print result1
getRouter('router3')
result2 = getRouter('router4')
print result2

print "\n\n[-for loop-]"

def getRouter2(rtr):
    router1 = {'os_version':'3.1.1', 'hostname':'nyc_router1', 'model':'nexus 9396', 'domain':'cisco.com', 'mgmt_ip':'10.1.50.11'}
    router2 = dict( os_version='3.2.1', hostname='rtp_router2', model='nexus 9396', domain='cisco.com', mgmt_ip='10.1.50.12')
    router2 = dict( os_version='3.1.1', hostname='ROUTER3', model='nexus 9504', domain='lab.cisco.com', mgmt_ip='10.1.50.13')
    router_list = [router1,router2,router3]
    for router in router_list:
        if rtr == router['hostname']:
            return router
    return 'No router found.'

result1 = getRouter2('nyc_router1')
print "function call" + result1

getRouter2('router_blob')
result2 = getRouter2('ROUTER3')

result2 = getRouter2('ROUTER3')
print result2

print "1.1.2 - END"
