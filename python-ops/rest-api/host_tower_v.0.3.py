import csv
import json,socket
import argparse
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth
import re
import subprocess
from email import Encoders
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase




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






fich = open("env.json","r")
#headers = {'Content-Type': 'application/json','Authorization':'Bearer S8qGItb7fe1VwFjX8yX3aH96BXHWdK' }
tempd = json.load(fich)
prod = tempd["prod"]
stage = tempd["stage"]

def hosts(data):
    ips=[]
    i=0
    while True:
        	try:
	        	ip=data["results"][i]["name"]
		        ips.append(ip)
		        i=i+1
	        except:
		               break
    return ips

parser = argparse.ArgumentParser()
parser.add_argument("-e")
args=parser.parse_args()
if args.e == "prod":
	headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%prod[1] }
	r = requests.get('%s/api/v2/hosts'%prod[0], headers=headers)
	data = json.loads(r.text)
	hosts= hosts(data)
	current_time=datetime.now()
	date_format=current_time.strftime("%Y-%m-%d-%H-%M-%S")
	namefile="%s.csv" %(date_format)
	with open(namefile, "a") as fl:
		opt=csv.writer(fl, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		opt.writerow(["IP"])
		for row in hosts:
	    		print row
			opt.writerow([row])
	mail(namefile)
elif args.e == "stage":
        headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%stage[1] }
        r = requests.get('%s/api/v2/hosts'%stage[0], headers=headers)
        data = json.loads(r.text)
        hosts= hosts(data)
        current_time=datetime.now()
        date_format=current_time.strftime("%Y-%m-%d-%H-%M-%S")
        namefile="%s.csv" %(date_format)
        with open(namefile, "a") as fl:
                opt=csv.writer(fl, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                opt.writerow(["IP"])
                for row in hosts:
                        print row
                        opt.writerow([row])
	mail(namefile)
else:
	print "missing arguments"
