##python script.py -i nodes.json 
#python script.py -d inventory -c instances

import subprocess
import argparse
import csv
import pandas as pd
import os,signal
import re
import  pymongo
from pymongo import MongoClient
import  json 
from  bson.json_util  import  dumps

def run(ip,usr,pwd,commands):
	#this function will run all commands and store the output in a list and return it
	dat = []
	for cmd in commands:
		p = subprocess.Popen(cmd ,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
		out, err=p.communicate()
		dat.append(out)
	for a in range(len(dat)):
		if not dat[a]:
			dat[a] = "NO"
		else:
			dat[a] = dat[a].rstrip('\n')
	return dat
def cmds(ip,usr,pwd):
	#this function will initialize all the commands and give them to run function for execution and return the output as well
	ip=str(ip)
	ip2 = "sshpass -p "+pwd+" ssh "+usr+"@"+ip+" "+"hostname -I | awk '{print $1;}'"
        host = "sshpass -p "+pwd+" ssh "+usr+"@"+ip+" "+"hostname -f"
        dist = "sshpass -p "+pwd+" ssh "+usr+"@"+ip+" "+"cat /etc/lsb-release | sed -n '2p' | cut -d "+"="+" -f2"
        cpu = "sshpass -p "+pwd+" ssh "+usr+"@"+ip+" "+"ps -A -o pcpu | tail -n+2 | paste -sd+ | bc"
        mem = "sshpass -p "+pwd+" ssh "+usr+"@"+ip+" "+"free -m | sed -n "+"'2p'"+" | awk "+"'{print $3;}'"
        ans = "sshpass -p "+pwd+" ssh "+usr+"@"+ip+" "+"ansible --version | sed -n '1p'"
        nginx ="sshpass -p "+pwd+" ssh "+usr+"@"+ip+" "+"\"sudo netstat -ntlp | grep 5432 | awk '{print \$4;}'| cut -d \":\" -f2\""
        pg = "sshpass -p "+pwd+" ssh "+usr+"@"+ip+" "+"\"sudo netstat -ntlp | grep 80 | sed -n '1p'| awk '{print \$4}' | cut -d \":\" -f2 \""
        cmd = [ip2,host,dist,cpu,mem,ans,pg,nginx]
	dat = run(ip,usr,pwd,cmd)
	return dat
def db_connect(db,coll):
#this function will get data from the db in   json format and return it if -c and -d parameters are correct
              client = MongoClient("mongodb://sys:iis123@127.0.0.1/inventory")
              db = client[db]
              # acquire inventory collection 
              data = db[coll].find({})[0]
              output_dict  =  {}
              # acquire inventory collection 
              output_dict.update(data)
              # Remove object ID
              del output_dict["_id"]
              # Dictionary by JSON format to standard output 
              return json.dumps(output_dict,indent=4)



def json_read_file(json_file):
#this function will get all hosts ,usernames and passwords and pass them for execution , after the execution it'll print the output and write to csv file 
        f = open(json_file,"r+")
        datax = json.load(f)
        keyz = datax.keys()
        sample=open("sampleReport.csv", "w")
        sample.write("")
        sample.close()
        status_machine=[]
        with open("sampleReport.csv", "a") as fl:
                dataS=csv.writer(fl, delimiter=",")
                dataS.writerow(["IP","HOSTNAME","OS VERSION","CPU USAGE","MEMORY USAGE","ANSIBLE VERSION","NGINX STATUS","DB STATUS"])
                for i in range(0,len(keyz)):
                        try:
                                hosts = datax[keyz[i]]["hosts"]
                                user = datax[keyz[i]]["vars"]["ansible_ssh_user"]
                                psw = datax[keyz[i]]["vars"]["ansible_ssh_pass"]
                                for ip in hosts:
                                        data=cmds(ip,user,psw)
                                        data = iter(data)
                                        dataS.writerow([str(next(data)).replace("\n",""), str(next(data)).replace("\n",""),str(next(data)).replace("\n",""),str(next(data)).replace("\n",""), str(next(data)).replace("\n",""),str(next(data)).replace("\n",""),str(next(data)).replace("\n",""), str(next(data)).replace("\n","")])
                                        continue
                        except:
                                continue
        rData=pd.read_csv("sampleReport.csv", index_col="IP")
        rData=rData.fillna("NO")
        rData["DB STATUS"].replace("\.0", "", regex=True, inplace=True)
        print rData
        print("Report generated, pls check  sampleReport.csv in your current Dir\n")
def json_read_db(db,coll):
#this function will get all hostnames,usernames and passwords and pass them for execution, after execution it'll print output and write to csv
        dax = db_connect(db,coll)
        datax = json.loads(dax)
        keyz = datax.keys()
        sample=open("sampleReport.csv", "w")
        sample.write("")
        sample.close()
        status_machine=[]
        with open("sampleReport.csv", "a") as fl:
                dataS=csv.writer(fl, delimiter=",")
                dataS.writerow(["IP","HOSTNAME","OS VERSION","CPU USAGE","MEMORY USAGE","ANSIBLE VERSION","NGINX STATUS","DB STATUS"])
                for i in range(0,len(keyz)):
                        try:
                                hosts = datax[keyz[i]]["hosts"]
                                user = datax[keyz[i]]["vars"]["ansible_ssh_user"]
                                psw = datax[keyz[i]]["vars"]["ansible_ssh_pass"]
                                for ip in hosts:
                                        data=cmds(ip,user,psw)
                                        data = iter(data)
                                        dataS.writerow([str(next(data)).replace("\n",""), str(next(data)).replace("\n",""),str(next(data)).replace("\n",""),str(next(data)).replace("\n",""), str(next(data)).replace("\n",""),str(next(data)).replace("\n",""),str(next(data)).replace("\n",""), str(next(data)).replace("\n","")])
                                        continue
                        except:
                                continue
        rData=pd.read_csv("sampleReport.csv", index_col="IP")
        rData=rData.fillna("NO")
        rData["DB STATUS"].replace("\.0", "", regex=True, inplace=True)
        print rData
        print("Report generated, pls check  sampleReport.csv in your current Dir\n")
if __name__ == '__main__':
#here will be arguments control and initialisation
	parser = argparse.ArgumentParser()
	parser.add_argument("-i")
	parser.add_argument("-c")
	parser.add_argument("-d")
	args = parser.parse_args()
	if (args.i is not None) and (args.c is None) and (args.d is None):
		json_read_file(args.i)
	elif (args.i is None) and (args.c is not None) and (args.d is not None):
		json_read_db(args.d,args.c)
	else:
		print "Missing arguments ."
