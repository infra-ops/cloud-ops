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

 	acs=[] 
        ipx=[] #ip
        nodeV=[]#host
        versionAns=[] #version
        cpuUsage=[]#cp Usage
        memUsage=[] #mem Usage
        ansVersion=[] #ans Version

	for x in re.findall(r'\b(ok\: \[.*\]).*\[debug\]',new_data,re.U): 
		data=(x.replace("ok: ["," ").replace("]","")) 
         	drt=data.split(" ")
         	for x in drt: 
             		acs.append(x)

        #---------------------------------Ac---------------------
        #for x in range(20):
         #   acs.append("ac"+str(x))
                
        for service in reversed(acs):
            #print(service)
            ipx.append(re.findall(r'ok: \['+service+'\]"ansible_default_ipv4.address": "[0-9]{2,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}', new_data))
#            ok: [ac1]"ansible_nodename": "controller"}ok: [ac2]"ansible_nodename": "an1"
            nodeV.append(re.findall(r'ok: \['+service+'\]"ansible_nodename": "ip-[0-9]{2,3}-[0-9]{1,3}-[0-9]{1,3}-[0-9]{1,3}', new_data))
            versionAns.append(re.findall(r'ok: \['+service+'\]"msg": "os version : [0-9]{1,3}.[0-9]{1,3}', new_data))
            cpuUsage.append(re.findall(r'ok: \['+service+'\]"msg": "cpu usage : [0-9]{1,3}.[0-9]{1,3}%', new_data))
            memUsage.append(re.findall(r'ok: \['+service+'\]"msg": "mem usage : [0-9]{1,6}',new_data))
            ansVersion.append(re.findall(r'ok: \['+service+'\]"msg": "ansible version : ansible [0-9]{1,2}.[0-9]{1,2}.[0-9]{1,2}', new_data))
       

	#ok: [127.0.0.1]"ansible_default_ipv4.address": "172.31.7.159"}ok: [172.31.7.159]"ansible_default_ipv4.address": "172.31.7.159"}
	
	acs1=list(reversed(acs))
	
        try:
		with  open("sample.csv", "a") as file:
        		ansible_data=csv.writer(file, delimiter=",")
            		#headers is not but will put just for test
            		ansible_data.writerow(["IP","HOSTNAME","OS VERSION","CPU USAGE","MEMORY USAGE","ANSIBLE VERSION"])
            		#---iter to extract data ------
            		for x in range(len(acs)):
                		ansible_data.writerow(["%s" %(str(re.findall(r'[0-9]{2,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}',str(ipx[x])[44:].replace("\']",""))).replace("[\'","").replace("\']","")),"%s" %(acs1[x]),"%s" %(str(re.findall(r'[0-9]{1,3}.[0-9]{1,3}',str(versionAns[x])[32:].replace("\']",""))).strip("][").strip("\'")),"%s" %(str(re.findall(r'[0-9]{1,3}.[0-9]{1,3}%',str(cpuUsage[x])[31:].replace("\']",""))).strip("\'").strip("][")),"%s" %(str(re.findall(r'[0-9]{1,6}',str(memUsage[x])[31:].replace("\']", ""))).strip("\'").strip("][")), "%s" %(str(re.findall(r'ansible [0-9].[0-9]{1,2}.[0-9]{1,2}',str(ansVersion[x])[37:].replace("\']", ""))).strip("\'").strip("]["))])
        	print("Done: data saved into sample.csv")
        except FileNotFoudError as ff_er:
		print("Error file not foud %s", format . ff_er)


"""
        for x in range(len(acs)):
                print(re.findall(r'[0-9]{2,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}',str(ipx[x])[44:].replace("\']","")))
                #print(re.findall(r'controller',str(nodeV[x])[32:].replace("\']","")))
                print(acs1[x])
                print(re.findall(r'[0-9]{1,3}.[0-9]{1,3}',str(versionAns[x])[32:].replace("\']","")))
                print(re.findall(r'[0-9]{1,3}.[0-9]{1,3}%',str(cpuUsage[x])[31:].replace("\']","")))
                print(re.findall(r'[0-9]{1,6}',str(memUsage[x])[31:].replace("\']", "")))
                print(re.findall(r'ansible [0-9].[0-9]{1,2}.[0-9]{1,2}',str(ansVersion[x])[37:].replace("\']", "")))
                print("\ndone!")
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
