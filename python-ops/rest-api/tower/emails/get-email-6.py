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





def mail():
         msg = MIMEMultipart()
	 msg["From"] = "me@example.com"
	 msg["To"] = "sudipta1436@gmail.com"
	 msg["Subject"] = "Report Ansible."
         part = MIMEBase('application', "octet-stream")
       	 part.set_payload(open("report-mail.csv", "rb").read())
	 Encoders.encode_base64(part)
         part.add_header('Content-Disposition', 'attachment', filename="report-mail.csv")
         msg.attach(part)
         p =subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
	 p.communicate(msg.as_string())
def one(data):
	mail_n=len(data["results"])
	mails=[]
	for k in range(0,mail_n):
                ma = data["results"][k]["email"]
                mails.append(ma)
	return mails
def get_email():
	page=1
	mails=[]
	while True:
		url = 'http://localhost/api/v2/users/?page=%s&page_size=100'%page
		r = requests.get(url, auth=HTTPBasicAuth('admin', 'password'))
		data = json.loads(r.text)
		try:
			if data["next"] == "null":
				mails=mails+one(data)
				return mails
			else:
				mails=mails+one(data)
				page=page+1
		except:
			return mails
all_mails = get_email()

ff = open("report-mail.csv","w+")
writer = csv.writer(ff)
writer.writerow(["users mail"])
for m in all_mails:
    writer.writerow([m])
    print(m + ",")
ff.close()

"""
for mail in emails:
    #mails = '' + str(mail) + ','
    print(mail + ",")

"""
mail()
