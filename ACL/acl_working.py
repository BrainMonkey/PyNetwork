from ipaddress import IPv4Address, IPv4Network
import socket, struct, sys


#asa interfaces
mon_networks = [IPv4Network(x) for x in [ u'10.101.0.0/24', u'10.101.1.0/24', u'10.101.4.0/24', u'10.101.8.0/24', u'10.101.12.0/24', u'10.101.15.0/24', u'10.101.20.0/24', u'10.102.20.128/25', u'10.110.0.35/32', u'10.110.0.36/32', u'10.110.1.0/24', u'10.190.10.0/24', u'10.200.1.0/24', u'10.201.12.0/24', u'10.255.0.0/24', u'12.22.179.16/28', u'63.99.120.0/22', u'66.180.2.16/28', u'66.180.7.48/28', u'172.21.1.0/24']]

inside_networks = [IPv4Network(x) for x in [ u'10.110.112.0/24']]

vpn_networks = [IPv4Network(x) for x in [ u'10.110.50.0/24']]


#interface checker
def AsaInt(ip, ip_list):
    # True if ip is in a reserved range, otherwise False
    ip = IPv4Address(ip)
    return any((ip in net) for net in ip_list)

#subnet calc
def cidr(prefix):
    return socket.inet_ntoa(struct.pack(">I", (0xffffffff << (32 - prefix)) & 0xffffffff))

#create new acl for each source IP
#def h2h_acl(acl_line, acl_name, sdm_num):
#	for i in acl_line:
#		print "access-list " + acl_name + " remark ********** START %s **********" % sdm_num
#		print "access-list " + acl_name + " extended permit %s host %s host %s eq %s" % (protocol,source_ip,dest_ip,port_num)
#		print "access-list " + acl_name + " remark ********** END %s  **********" % sdm_num
#		
#def h2s_acl(acl_line, acl_name, sdm_num):
#	for i in acl_line:
#		print "access-list " + acl_name + " remark ********** START %s **********" % sdm_num
#		print "access-list " + acl_name + " extended permit %s host %s %s %s eq %s" % (protocol,source_ip,dest_ip,dest_mask,port_num)
#		print "access-list " + acl_name + " remark ********** END %s  **********" % sdm_num
#		
#def s2h_acl(acl_line, acl_name, sdm_num):
#	for i in acl_line:
#		print "access-list " + acl_name + " remark ********** START %s **********" % sdm_num
#		print "access-list " + acl_name + " extended permit %s %s %s host %s eq %s" % (protocol,source_ip,source_mask,dest_ip,port_num)
#		print "access-list " + acl_name + " remark ********** END %s  **********" % sdm_num
#		
#def s2s_acl(acl_line, acl_name, sdm_num):
#	for i in acl_line:
#		print "access-list " + acl_name + " remark ********** START %s **********" % sdm_num
#		print "access-list " + acl_name + " extended permit %s %s %s %s %s eq %s" % (protocol,source_ip,source_mask,dest_ip,dest_mask,port_num)
#		print "access-list " + acl_name + " remark ********** END %s  **********" % sdm_num
		
def acl(source_ip, acl_name, sdm_num,protocol, srcIPconfig, dstIPconfig, port_num):
	for i in source_ip:
		
		print "\naccess-list " + acl_name + " remark ********** START " + sdm_num + "**********" 
		print "access-list " + acl_name + "extended permit " + protocol + " " + srcIPconfig + " " + dstIPconfig + " eq " + port_num
		print "access-list " + acl_name + " remark ********** END " + sdm_num + "**********\n" 
		
def IPInfo(IPAddr, IPMask):
	if IPMask == "32":
		return("host " + IPAddr)
	else:
		return(IPAddr + " " + str(cidr(int(IPMask))))
	
def ACLname(source_ip):
	if AsaInt(unicode(source_ip), mon_networks) == True:
		return " mon_access_in "
	elif AsaInt(unicode(source_ip), inside_networks) == True:
		return " inside_access_in "
	elif AsaInt(unicode(source_ip), vpn_networks) == True:
		return " vpn_access_in "
	else:
		return " outside_access_in "

should_restart = True
while should_restart:
	should_restart = False
	source_ip = raw_input("please enter a source IP's: ")
	
	
	source_cidr = raw_input("source IP CIDR?: ")
	#source_mask= str(cidr(int(source_cidr)))
	dest_ip = raw_input("please enter a destination IP: ")
	dest_cidr = raw_input("dest IP CIDR?: ")
	#dest_mask = str(cidr(int(dest_cidr)))
	protocol = raw_input("TCP, UDP or IP?: ")
	port_num = raw_input("please enter the port number: ")
	sdm_num = raw_input("please enter the SDM number: ")

	srcIPconfig = IPInfo(source_ip, source_cidr)
	dstIPconfig = IPInfo(dest_ip, dest_cidr)
	acl_name = ACLname(source_ip)
	acl([source_ip],acl_name,sdm_num,protocol,srcIPconfig,dstIPconfig,port_num)
	
	
	start_over = raw_input("Need another ACL y or n? or type exit to quit: ")
	if start_over == 'y':
		should_restart = True
	else:
		
		break
	

	
#	if AsaInt(unicode(source_ip), mon_networks) == True:
#		acl_name = "mon_access_in"
#		acl([source_ip],acl_name,sdm_num,protocol,srcIPconfig,dstIPconfig,port_num)
#		start_over = raw_input("Need another ACL y or n? or type exit to quit: ")
#		if start_over == 'y':
#			should_restart = True
#		else:
#			break
#	elif AsaInt(unicode(source_ip), inside_networks) == True:
#		acl_name = "inside_access_in"
#		acl([source_ip],acl_name,sdm_num,protocol,srcIPconfig,dstIPconfig,port_num)
#		start_over = raw_input("Need another ACL y or n? or type exit to quit: ")
#		if start_over == 'y':
#			should_restart = True
#		else:
#			break
#	elif AsaInt(unicode(source_ip), vpn_networks) == True:
#		acl_name = "vpn_access_in"
#		acl([source_ip],acl_name,sdm_num,protocol,srcIPconfig,dstIPconfig,port_num)
#		start_over = raw_input("Need another ACL y or n? or type exit to quit: ")
#		if start_over == 'y':
#			should_restart = True
#		else:
#			break
#	else:
#		acl_name = "vpn_access_in"
#		acl([source_ip],acl_name,sdm_num,protocol,srcIPconfig,dstIPconfig,port_num)
#		start_over = raw_input("Need another ACL y or n? or type exit to quit: ")
#		if start_over == 'y':
#			should_restart = True
#		else:
#			break
#		
#	if source_cidr == "32" and dest_cidr == "32":
#		if AsaInt(unicode(source_ip), mon_networks) == True:
#			acl_name = "mon_access_in"
#			h2h_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		elif AsaInt(unicode(source_ip), inside_networks) == True:
#			acl_name = "inside_access_in"
#			h2h_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		elif AsaInt(unicode(source_ip), vpn_networks) == True:
#			acl_name = "vpn_access_in"
#			h2h_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		else:
#			acl_name = "outside_access_in"
#			h2h_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#	#host to subnet
#	elif source_cidr == "32":
#		if AsaInt(unicode(source_ip), mon_networks) == True:
#			acl_name = "mon_access_in"
#			h2s_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		elif AsaInt(unicode(source_ip), inside_networks) == True:
#			acl_name = "inside_access_in"
#			h2s_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		elif AsaInt(unicode(source_ip), vpn_networks) == True:
#			acl_name = "vpn_access_in"
#			h2s_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		else:
#			acl_name = "outside_access_in"
#			h2s_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#	#subnet to host
#	elif dest_cidr == "32":
#		if AsaInt(unicode(source_ip), mon_networks) == True:
#			acl_name = "mon_access_in"
#			s2h_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		elif AsaInt(unicode(source_ip), inside_networks) == True:
#			acl_name = "inside_access_in"
#			s2h_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		elif AsaInt(unicode(source_ip), vpn_networks) == True:
#			acl_name = "vpn_access_in"
#			s2h_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		else:
#			acl_name = "outside_access_in"
#			s2h_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#	#subnet to subnet	
#	else: 
#		if AsaInt(unicode(source_ip), mon_networks) == True:
#			acl_name = "mon_access_in"
#			s2s_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		elif AsaInt(unicode(source_ip), inside_networks) == True:
#			acl_name = "inside_access_in"
#			s2s_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		elif AsaInt(unicode(source_ip), vpn_networks) == True:
#			acl_name = "vpn_access_in"
#			s2s_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#		else:
#			acl_name = "outside_access_in"
#			s2s_acl([source_ip], acl_name, sdm_num)
#			start_over = raw_input("Need another ACL y or n?: ")
#			if start_over == 'y':
#				should_restart = True
#
#
#
#	#else:
#	#	break
			


	

