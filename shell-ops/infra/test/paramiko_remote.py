import os
import paramiko
import getpass

user=os.getlogin()
print "Connecting via %s: what is your password?" % user
pw = getpass.getpass()
ssh = paramiko.SSHClient()
#ssh.load_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('10.137.2.57', username='root', password='Dev0ps!@#')
stdin, stdout, stderr = ssh.exec_command('netstat -ntlp | grep 80')
print "output", stdout.read()
ssh.close()
