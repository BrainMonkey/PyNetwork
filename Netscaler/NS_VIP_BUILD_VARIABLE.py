import time, getpass
from nsnitro import *





# login
nitro = NSNitro('X.X.X.X', 'nsroot', getpass.getpass())
nitro.login()
print "starting to connect..."
print "connected."

SERVER_NAME = raw_input('please enter a server name:')

# add server test
addserver = NSServer()
addserver.set_name(SERVER_NAME)
addserver.set_ipaddress("5.5.5.5")
NSServer.add(nitro, addserver)
# get server status
server = NSServer()
#server.set_name("mp-nitroserver")
server = server.get(nitro, server)
print server.get_name() + ": " + server.get_state()

SVC_NAME = raw_input('please enter a service name:')

# add service test
addservice = NSService()
addservice.set_name(SVC_NAME)
addservice.set_servername(SERVER_NAME)
addservice.set_servicetype("HTTP")
addservice.set_port(11111)
NSService.add(nitro, addservice)

LB_NAME = raw_input('please enter a LB name:')
LB_IP = raw_input('please enter a IP name:')

# add lbvserver test
lbvserver = NSLBVServer()
lbvserver.set_name(LB_NAME)
lbvserver.set_ipv46(LB_IP)
lbvserver.set_port(11111)
lbvserver.set_clttimeout(180)
lbvserver.set_persistencetype("NONE")
lbvserver.set_servicetype("HTTP")
NSLBVServer.add(nitro, lbvserver)
#
print "LB vserver added"

# bind service to lbvserver test
lbbinding = NSLBVServerServiceBinding()
lbbinding.set_name(LB_NAME)
lbbinding.set_servicename(SVC_NAME)
lbbinding.set_weight(40)
NSLBVServerServiceBinding.add(nitro, lbbinding)

print "Binding added"

lbbinding = NSLBVServerServiceBinding()
lbbinding.set_name(LB_NAME) 
lbbindings = NSLBVServerServiceBinding.get(nitro, lbbinding)

for lbb in lbbindings:
        print "sgn: " + lbb.get_servicegroupname()
