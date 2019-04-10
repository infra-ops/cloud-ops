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

def work(ur,tok):
        page=1
        ips=[]
        while True:
                try:
                        headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%tok }
                        r = requests.get('%s/api/v2/hosts?page=%s&page_size=100'%(ur,page), headers=headers)
                        data = json.loads(r.text)
                        num = len(data["results"])
                        if data["next"] == "null":
                                for i in range(0,num):
                                        ip=data["results"][i]["name"]
                                        ips.append(ip)
                                break
                        else:
                                for i in range(0,num):
                                        ip=data["results"][i]["name"]
                                        ips.append(ip)
                                page=page+1
                except:
                        break
        current_time=datetime.now()
        date_format=current_time.strftime("%Y-%m-%d-%H-%M-%S")
        namefile="%s.csv" %(date_format)
        with open(namefile, "a") as fl:
                opt=csv.writer(fl, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                opt.writerow(["IP"])
                for row in ips:
                        print row
                        opt.writerow([row])
        mail(namefile)




fich = open("env.json","r")
#headers = {'Content-Type': 'application/json','Authorization':'Bearer S8qGItb7fe1VwFjX8yX3aH96BXHWdK' }
tempd = json.load(fich)
prod = tempd["prod"]
stage = tempd["stage"]

parser = argparse.ArgumentParser()
parser.add_argument("-e")
args=parser.parse_args()
if args.e == "prod":
	work(prod[0],prod[1])
elif args.e == "stage":
	work(stage[0],stage[1])
else:
	print "missing arguments"

