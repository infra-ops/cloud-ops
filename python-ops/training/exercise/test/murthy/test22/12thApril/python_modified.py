#!/usr/bin/python

import os
import paramiko

os.system("tput clear")
os.system("tput cup 3 15")
SSH='ssh -q -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
SOURCE='/opt/bash_sandbox/ril_send/*'
DEST='/opt/bash_sandbox/ril_receive'
RUSER='idcadm'
RPASS='redhat'
os.system("tput setaf 3")
os.system('echo "WELCOME TO THE WORLD OF AUTOMATION"')
os.system("tput sgr0")
os.system("tput cup 5 17")
# Set reverse video mode
os.system("tput rev")
os.system('echo "M A I N - M E N U"')
os.system("tput sgr0")

def menu():
    os.system("tput bold")
    os.system("tput cup 7 15")
    print "[1] PINGING STATUS OF NODES"
    os.system("tput cup 8 15")
    print "[2] COPY FOLDER TO LINUX NODES"
    os.system("tput cup 9 15")
    print "[3]  EXIT"
    os.system("tput cup 10 15")
    var = raw_input("Enter your menu choice [1-3]: \n")
    return var

def wait():
    pass

def ping_status():
    print "Ping"

    var = raw_input("ENTER SINGLE IP / IPLIST seperated by spaces: \n")
    
    if  var !="" and not var.isspace(): #not empty
        print "not blank"
        words = var.split()
        for  word in words:
            print word 
            hostname = word
            response = os.system("ping -c 1 " + hostname)
            #check the response...
            if response == 0:
                print hostname, 'is up!'
            else:
                print hostname, 'is down!'
    else:
        print "Please rerun"
  


def copy_file():
    print "in copy_file"
    
    user= raw_input("ENTER USER NAME:")
    
    print "ENTER PASSWORD : "
    os.system("stty -echo")
    password = raw_input("")
    os.system("stty echo;")
    ip_list= raw_input("ENTER SINGLE IP /IP LIST : \n")
    
    if  ip_list !="" and not ip_list.isspace(): #not empty
        print "not blank"
        ip_list = ip_list.split()
        for  ip in ip_list:
            ssh = paramiko.SSHClient()
            
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, username=user, password=password)
            stdin, stdout, stderr = ssh.exec_command("mkdir "+ DEST)
            exit_code = os.system("echo $?")
            print "Exit code is: "+str(exit_code)
            if  exit_code == 0:
                print stdout.readlines()
                os.system("sshpass -p "+ password+" scp "+SOURCE+" "+ user+"@"+ip+":"+DEST)
                exit_code = os.system("echo $?")
                print "Exit code is: "+str(exit_code)
        
        if exit_code != 0:
            os.system("sshpass -p " + password+" rsync -avz  "+ SOURCE+" "+user+"@"+ip+":"+DEST)
            exit_code = os.system("echo $?")
            print "Exit code is: "+str(exit_code)

    else:
        print "Please rerun"

def exit():
    print "In exit"
    os.system("exit 0")

# map the inputs to the function blocks
options = {
  '1' : ping_status,
  '2' : copy_file,
  '3' : exit,
}

var = menu()
os.system("tput cup 11 15")

options[var]()