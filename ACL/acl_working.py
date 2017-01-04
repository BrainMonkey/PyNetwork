from ipaddress import *
import socket
import struct
mon_networks = [IPv4Network(x) for x in [ '10.101.0.0/24',
                                          '10.101.1.0/24',
                                          '10.101.4.0/24',
                                          '10.101.8.0/24',
                                          '10.101.12.0/24',
                                          '10.101.15.0/24',
                                          '10.101.20.0/24',
                                          '10.102.20.128/25',
                                          '10.110.0.35/32',
                                          '10.110.0.36/32',
                                          '10.110.1.0/24',
                                          '10.190.10.0/24',
                                          '10.200.1.0/24',
                                          '10.201.12.0/24',
                                          '10.255.0.0/24',
                                          '12.22.179.16/28',
                                          '63.99.120.0/22',
                                          '66.180.2.16/28',
                                          '66.180.7.48/28',
                                          '172.21.1.0/24']]



inside_networks = [IPv4Network(x) for x in [ '10.110.112.0/24']]

vpn_networks = [IPv4Network(x) for x in [ '10.110.50.0/24']]




#interface checker
#compares 'ip' to an 'ip_list' (i.e. mon_networks)
def AsaInt(ip, ip_list):
    ip = IPv4Address(ip) #converts string or integer to ip address
    return any((ip in net) for net in ip_list) #this generator expression matches first match if it is contained in the list(i.e. mon_networks) and returns it as true

#subnet calc
#converts cidr to subnet mask
#credit to http://stackoverflow.com/questions/23352028/how-to-convert-a-cidr-prefix-to-a-dotted-quad-netmask-in-python
def cidr(prefix):
    return socket.inet_ntoa(struct.pack(">I", (0xffffffff << (32 - prefix)) & 0xffffffff))


#ACL creator
def acl(source_ip, acl_name, sdm_num,protocol, srcIPconfig, dstIPconfig, port_num):
	for i in source_ip:
		global X
		X = "access-list " + acl_name + "extended permit " + protocol + " " + srcIPconfig + " " + dstIPconfig + " eq " + port_num

def acl_startstop(acl_name):
		print ("\naccess-list " + acl_name + " remark ********** START " + sdm_num + "**********")
		print (X)
		print ("access-list " + acl_name + " remark ********** END " + sdm_num + "**********\n")

def IPInfo(IPAddr, IPMask):
	if IPMask == "32":
		return("host " + IPAddr)
	else:
		return(IPAddr + " " + str(cidr(int(IPMask))))

def ACLname(source_ip):
    #if source_ip is in IP list (i.e. mon, inside, vpn) match it to the ACL name
	if AsaInt((source_ip), mon_networks) == True:
		return " mon_access_in "
	elif AsaInt((source_ip), inside_networks) == True:
		return " inside_access_in "
	elif AsaInt((source_ip), vpn_networks) == True:
		return " vpn_access_in "
	else:
		return " outside_access_in "

while True:
	source_ip = input("please enter a source IP's: ")
	source_cidr = input("source IP CIDR?: ")
	dest_ip = input("please enter a destination IP: ")
	dest_cidr = input("dest IP CIDR?: ")
	protocol = input("TCP, UDP or IP?: ")
	port_num = input("please enter the port number: ")
	sdm_num = input("please enter the SDM number: ")

    #Adds 'Host' syntax to ACL line based on '32' CIDR notation
	srcIPconfig = IPInfo(source_ip, source_cidr)
	dstIPconfig = IPInfo(dest_ip, dest_cidr)

    #matches source IP to ACL name
	acl_name = ACLname(source_ip)

	start_over = input("Need another ACL y or n? or type exit to quit: ")


	acl([source_ip],acl_name,sdm_num,protocol,srcIPconfig,dstIPconfig,port_num)


	if "mon_access_in" or "inside_access_in" or "vpn_access_in" or "outside_access_in" in X:
		acl_startstop(acl_name)
	else:
		break







