from ssh_list_test import ssh_host
import getpass, time




USER = getpass.getuser()
time.sleep(1)
PASSWORD = getpass.getpass()
IPS = 'X.X.X.X'
cmdList = ["terminal length 0", "sh vlan | i 1691", "sh run | i 1691", "exit"]



ssh_host(IPS, USER, PASSWORD, cmdList)
