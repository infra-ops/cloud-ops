#!/usr/bin/python
#python security-check-8.py  -i /etc/ansible/inventories/generic/static/local/local.yml -f /etc/ansible/playbooks/patchman/log-check.yml







import re
import json
from datetime import datetime as dt
import subprocess
import argparse
import boto3
import csv
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

def sendLogFileEmail(log_file, log_data):
	message = MIMEMultipart()
	message['Subject'] = log_file
	message['From'] = 'chakraborty.rock@gmail.com'
	message['To'] = 'sudipta1436@gmail.com'
	message.preamble = 'Multipart message.\n'
	message.attach(MIMEText('status of service'))	
	part = MIMEApplication(log_data)
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % log_file)
	message.attach(part)
	client = boto3.client('ses')
	response = client.send_raw_email (Source='chakraborty.rock@gmail.com',Destinations=['sudipta1436@gmail.com'],RawMessage={'Data': message.as_string()})


def execute(fur,sur):
                cmd2 = "ansible-playbook -i %s %s"%(fur,sur)
                p = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)  
                out, err = p.communicate()
		print out

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser()
	parser.add_argument("-i")
	parser.add_argument("-f")
	args = parser.parse_args()
	if (args.i is not None) and (args.f is not None):
		execute(args.i,args.f)
	else:
		print "Missing arguments ."
