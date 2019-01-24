#!/usr/bin/env python3
#python security-check-8.py  -i /etc/ansible/inventories/generic/static/local/local.yml -f /etc/ansible/playbooks/patchman/log-check.yml
import re
import json
from datetime import datetime as dt
import subprocess
import argparse
import csv


def gencsv(out):
       # out=out.read()
        new_data=str(out).replace("\n","").replace("*","").replace("=> {","").replace("     ","")
        print(new_data)
        print("\n")

        acs=[] #number of service
        ipx=[] #ip
        nodeV=[]#host
        versionAns=[] #version
        cpuUsage=[]#cp Usage
        memUsage=[] #mem Usage
        ansVersion=[] #ans Version


        #---------------------------------Ac---------------------
        for x in range(20):
            acs.append("ac"+str(x))
                
        for service in acs:
            ipx.append(re.findall(r'ok: \['+service+'\]"ansible_default_ipv4.address": "[0-9]{2,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', new_data))
#            ok: [ac1]"ansible_nodename": "controller"}ok: [ac2]"ansible_nodename": "an1"
            nodeV.append(re.findall(r'ok: \['+service+'\]"ansible_nodename": "[a-z]+\w[0-9]{1,3}', new_data))
            versionAns.append(re.findall(r'ok: \['+service+'\]"msg": "os version : [0-9]{1,3}.[0-9]{1,3}', new_data))
            cpuUsage.append(re.findall(r'ok: \['+service+'\]"msg": "cpu usage : [0-9]{1,3}.[0-9]{1,3}%', new_data))
            memUsage.append(re.findall(r'ok: \['+service+'\]"msg": "mem usage : [0-9]{1,6}',new_data))
            ansVersion.append(re.findall(r'ok: \['+service+'\]"msg": "ansible version : ansible [0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2}', new_data))
       
       
        with  open("result.csv", "a") as file:
            ansible_data=csv.writer(file, delimiter=",")
            #headers is not but will put just for test
            ansible_data.writerow(["IP","HOSTNAME","OS VERSION","CPU USAGE","MEMORY USAGE","ANSIBLE VERSION"])
            #---iter to extract data ------
            for x in range(20):

                ansible_data.writerow(["%s" %(str(ipx[x])[44:].replace("\']","")),"%s" %(str(nodeV[x])[32:].replace("\']","")),"%s" %(str(versionAns[x])[32:].replace("\']","")), "%s" %(str(cpuUsage[x])[31:].replace("\']","")),"%s" %(str(memUsage[x])[31:].replace("\']", "")), "%s" %(str(ansVersion[x])[37:].replace("\']", ""))])
         
        
        #----iter to extract data---------
"""
        for x in range(20):
            print(str(ipx[x])[44:].replace("\']",""))
            #print(str(nodeV[x])[32:].replace("\']",""))
            print(str(versionAns[x])[32:].replace("\']",""))
            print(str(cpuUsage[x])[31:].replace("\']",""))
            print(str(memUsage[x])[31:].replace("\']", ""))
            print(str(ansVersion[x])[37:].replace("\']", ""))
"""


def execute(fur,sur):
		cmd2 = "ansible-playbook -i %s %s"%(fur,sur)
		p = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
		out, err = p.communicate()
		return(out)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-i")
	parser.add_argument("-f")
	args = parser.parse_args()
	if (args.i is not None) and (args.f is not None):
		out = execute(args.i,args.f)
		gencsv(out)
	else:
		print("Missing arguments .")
