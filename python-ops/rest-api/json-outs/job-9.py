import csv
import json,socket
import requests
import re
import argparse
from datetime import datetime
from requests.auth import HTTPBasicAuth
import re
import subprocess
from email import Encoders
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from ansible.constants import DEFAULT_VAULT_ID_MATCH
from ansible.parsing.vault import VaultLib
from ansible.parsing.vault import VaultSecret
from termcolor import colored


"""
def color():
    RED   = "\033[1;31m"  
    GREEN = "\033[0;32m"

"""



def mail(report):
         msg = MIMEMultipart()
	 msg["From"] = "me@example.com"
	 msg["To"] = "sudipta1436@gmail.com"
	 msg["Subject"] = "Report Ansible."
         part = MIMEBase('application', "octet-stream")
       	 part.set_payload(open(report, "rb").read())
	 Encoders.encode_base64(part)
         part.add_header('Content-Disposition', 'attachment', filename=report)
         msg.attach(part)
         p =subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
	 p.communicate(msg.as_string())
	 #print "done"
def work(uro,tok,data):
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
	i=0
	while True:
		try:
       	               temp = data["results"][i]["name"]
	               proj=data["results"][i]["project"]
	               sta = data["results"][i]["status"]
	               #fetch project name
	               u2 = "%s/api/v2/projects/%s/?page_size=100"%(uro,str(proj))
                       r2 = requests.get(u2,headers=headers,verify=False)
	               data2 = json.loads(r2.text)
	               pname = data2["name"]
	               gb=pname.split("_")[0]
	               gf=pname.split("_")[1]
	               #fetch launcher name
	               page_ur=data["results"][i]["related"]["created_by"]
	               u3 = "%s%s"%(uro,str(page_ur))
		       r3 = requests.get(u3,headers=headers,verify=False)
	               data3 = json.loads(r3.text)
	               uname = data3["username"]
	               print colored("%s\t%s\t%s\t%s\t%s\t%s"%(gb,gf,pname,temp,sta,uname),'red')
	               writing.writerow([pname,temp,sta,uname])
	               i=i+1
		except:
			break
ff = open("report3.csv","w+")
writing = csv.writer(ff)
writing.writerow(["GB\tGF\tPROJECT_NAME","JOB_NAME","STATUS","LAUNCHER"])
print colored("GB\tGF\tPROJECT_NAME\tJOB_NAME\tSTATUS\tLAUNCHER", 'red')


vault = VaultLib([(DEFAULT_VAULT_ID_MATCH, VaultSecret('tower@123'))])
fich =  vault.decrypt(open('/home/nik/Desktop/git-repo/cloud-ops/python-ops/rest-api/json-outs/env-1.json').read())
#fich = open("env.json","r")
#headers = {'Content-Type': 'application/json','Authorization':'Bearer S8qGItb7fe1VwFjX8yX3aH96BXHWdK' }
tempd = json.loads(fich)
prod = tempd["prod"]
stage = tempd["stage"]
page = 1
parser = argparse.ArgumentParser()
parser.add_argument("-e")
args=parser.parse_args()
if args.e == "prod":
	ur=prod[0]
	toke=prod[1]
	headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%toke }
	while True:
		try:
	        	u1 = '%s/api/v2/jobs/?job_type=run&launch_type=manual&page=%s&started__gt=2019-03-20T00:00&started__lt=2019-03-26T00:00&page_size=100'%(ur,page)
        	        r1 = requests.get(u1,headers=headers,verify=False)
		        data=json.loads(r1.text)
			if data["next"]=="null":
				work(ur,toke,data)
				break
			else:
				work(ur,toke,data)
				page=page+1
		except:
			break
	ff.close()
	mail("report3.csv")
elif args.e == "stage":
	ur=stage[0]
	toke=stage[1]
	headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%toke }
        while True:
                try:
                        u1 = '%s/api/v2/jobs/?job_type=run&launch_type=manual&page=%s&started__gt=2019-03-20T00:00&started__lt=2019-03-26T00:00&page_size=100'%(ur,page)
                        r1 = requests.get(u1,headers=headers,verify=False)
                        data=json.loads(r1.text)
                        if data["next"]=="null":
                                work(ur,toke,data)
                                break
                        else:
                                work(ur,toke,data)
                                page=page+1
                except:
                        break
	ff.close()
	mail("report3.csv")
else:
	print "missing arguments"
