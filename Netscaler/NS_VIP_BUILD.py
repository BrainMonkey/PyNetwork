
import time, getpass
from nsnitro import *

# login
nitro = NSNitro('X.X.X.X', 'nsroot', getpass.getpass())
nitro.login()

# add server test
addserver = NSServer()
addserver.set_name("MARTER-TEST01")
addserver.set_ipaddress("5.5.5.5")
NSServer.add(nitro, addserver)
# get server status
server = NSServer()
#server.set_name("mp-nitroserver")
server = server.get(nitro, server)
print server.get_name() + ": " + server.get_state()

# add service test
addservice = NSService()
addservice.set_name("MARTER-SVC01")
addservice.set_servername("MARTER-TEST01")
addservice.set_servicetype("HTTP")
addservice.set_port(11111)
NSService.add(nitro, addservice)

# add lbvserver test
lbvserver = NSLBVServer()
lbvserver.set_name("MARTER-LB01")
lbvserver.set_ipv46("10.32.110.55")
lbvserver.set_port(11111)
lbvserver.set_clttimeout(180)
lbvserver.set_persistencetype("NONE")
lbvserver.set_servicetype("HTTP")
NSLBVServer.add(nitro, lbvserver)
#
print "LB vserver added"

# bind service to lbvserver test
lbbinding = NSLBVServerServiceBinding()
lbbinding.set_name("MARTER-LB01")
lbbinding.set_servicename("MARTER-SVC01")
lbbinding.set_weight(40)
NSLBVServerServiceBinding.add(nitro, lbbinding)

print "Binding added"

lbbinding = NSLBVServerServiceBinding()
lbbinding.set_name("MARTER-LB01")
lbbindings = NSLBVServerServiceBinding.get(nitro, lbbinding)

for lbb in lbbindings:
        print "sgn: " + lbb.get_servicegroupname()
