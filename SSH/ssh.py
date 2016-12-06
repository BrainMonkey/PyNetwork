import paramiko, time, re, csv, sys, getpass, difflib, os
from os import listdir
from os.path import isfile, join


def ssh_host(hostName, userName, userPassword, cmdList):

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #auto accept host keys
            client.connect(hostName, username=userName, password=userPassword)

        except IOError as e:
                                print "Could not connect to %s error %s" % (hostName, e)
        else:
                                print "connected to %s \n" % hostName
                                channel = client.invoke_shell()
                                time.sleep(1)
                                for cmd in cmdList:
                                        channel.send( cmd + "\n")
                                time.sleep(1)
                                stdout = channel.makefile('rb')
                                fout = open(hostName + '_ssh_output.txt', 'w')
                                line = stdout.read()
                                print fout, "/n", line
                                fout.write(line)
                                fout.close()
                                channel.close()

if __name__ == "__main__":
        main()