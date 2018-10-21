#!/usr/bin/env python

#execution process

#python security-check-2.py	-i	/root/keys3/id_rsa	-n sudipta@xxxxx
#python security-check-2.py	-i	/root/keys3/id_rsa	-u sudipta -n 52.xx.xx.xx
#python security-check-2.py	-i	/root/keys3/id_rsa	-u sudipta -f nodes.json

import re
import json
from datetime import datetime as dt
import subprocess
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

	# what a recipient sees if they don't use an email reader
	message.preamble = 'Multipart message.\n'

	# the message body
	message.attach(MIMEText('status of service'))	
	part = MIMEApplication(log_data)
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % log_file)
	message.attach(part)
	client = boto3.client('ses')
	response = client.send_raw_email (Source='chakraborty.rock@gmail.com',Destinations=['sudipta1436@gmail.com'],RawMessage={'Data': message.as_string()})
	##print "E-mail sent: " + str(response)

def security (json_input, ips, user, pem):
	log_content = [["date", "ip", "patches"]]
	send_email = False

	if ips != None:
		for ip in ips:
			patches = security_check(ip, user, pem)
			if "@" in ip:
				ip = ip.split("@")[1]
			try:
				if int(patches.strip()) > 0:
					log_content.append([dt.today().date().isoformat(), ip, str(patches)])
					send_email = True
			except:
				pass

	if json_input != None:
		for region in json_input.keys():
			for ip in json_input[region]:
				patches = security_check(ip, user, pem)
				if "@" in ip:
					ip = ip.split("@")[1]
				try:
					if int(patches.strip()) > 0:
						log_content.append([dt.today().date().isoformat(), ip, str(patches)])
						send_email = True
				except:
					pass

	file_name = "{}.csv".format(dt.now().isoformat()[:-7].replace("T", "-").replace(":", "-"))
	
	output = open(file_name, "wb")
	writer = csv.writer(output)
	writer.writerows(log_content)
	output.close()

	for row in log_content:
		print ", ".join(row)

	if send_email is True:
		sendLogFileEmail(file_name, open(file_name).read())

def	security_check(ip, user, pem):
	if "@" in ip:
		user = ip.split("@")[0]
		ip	 = ip.split("@")[1]

	cmd = 'ssh -i {} {}@{} "/usr/lib/update-notifier/apt-check 2>&1 | cut -d'.format(pem, user, ip) + "';'" + ' -f2-"'

	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	out, err = p.communicate()

	#print "Command: {}".format(cmd)
	#print "Output: {}".format(out)
	#rint "Error: {}".format(err)
	if out == "":
		out = "NA"

	return out

if __name__ == '__main__':
	import argparse
	
	parser = argparse.ArgumentParser(description='Receive the input file directory.')
	parser.add_argument("-f", dest="input_file", nargs="?", metavar='N', type=str, help="file contains eips which are need to be released")
	parser.add_argument("-n", dest='ip', nargs="*", help="security check on single node")
	parser.add_argument("-u", dest='user', nargs=1, type=str, help="user to login")
	parser.add_argument("-i", dest='pem', nargs=1, type=str, help="path to .pem file")

	args = parser.parse_args()
	json_file, ip = None, None
		
	try:
		file = open(args.input_file)
		json_file = json.loads(file.read())
	except:
		pass

	ip	 = args.ip
	user = args.user
	pem	= args.pem

	if user != None:
		user = user[0]
	if pem != None:
		pem = pem[0]

	security(json_file, ip, user, pem)
	
#def lambda_handler(event, context):
#	release_eip(event, None)
