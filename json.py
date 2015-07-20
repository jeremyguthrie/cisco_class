router = {}
router['hostname'] = 'router1'
router['location'] = 'nyc'
router['vrf'] = 'production'
router['domain'] = 'cisco.com'
router['os_version'] = '3.1.2'
print router
import json
print json.dumps(router, indent=4)
router1 = router
router2 = {'os_version': '3.1.2', 'domain': 'cisco.com', 'hostname': 'router2', 'location': 'nyc', 'vrf': 'production'}
router3 = {'os_version': '3.1.2', 'domain': 'cisco.com', 'hostname': 'router3', 'location': 'nyc', 'vrf': 'production'}
neighbors = [ router2, router3 ]
print neighbors
router1['neighbors'] = neighbors
print json.dumps(router, indent=4)

print router1['neighbors'][0]['hostname']

for key,value in router1.iteritems():
    print 'KEY: ', key
    print 'value: ', value
    print '=' * 20


for key,value in router1.iteritems():
    if key == 'neighbors':
        print value
        for each in value:
            for k,v in each.iteritems():

for key,value in router1.iteritems():
    if key == 'neighbors':
        for each in value:
            print each['hostname']
                if k == 'hostname':
                    print v

for key,value in router1.iteritems():
     if key == 'neighbors':
         for each in value:
             print each['hostname']

for key,value in router1.iteritems():
     if key == 'neighbors':
         for each in value:
             print each
