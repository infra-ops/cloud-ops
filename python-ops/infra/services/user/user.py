#!/usr/bin/python
import datetime
import sys
import subprocess

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

f_live = open("status_ok_" + current_time_string  + ".html" , "w")
f_dead = open("status_err_" + current_time_string  + ".html", "w")

arg = sys.argv[1:]

#ssh -i meso/m1.txt root@172.16.55.141 "useradd -m user7"
#python user.py /root/meso/m1.txt root 172.16.55.141 user7

def tuser(arg):
    cmd = 'ssh -i '+arg[0]+' '+arg[1]+'@'+arg[2]+' "useradd -m '+arg[3]+'"'
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    #print output
    if output:
        r1 = 'user created successfully at ' + arg[3]
        f_live.write(r1)
    else:
        r1 = 'user not created successfully at '+ arg[3]
        f_dead.write(r1)

        
tuser(arg)
#print len(arg)
#print arg[0]
