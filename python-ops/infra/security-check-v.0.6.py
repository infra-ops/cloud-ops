#!/usr/bin/env python
#python security-check-2.py	-i	/root/keys3/id_rsa	-u sxxxxx -n 52.xx.xx.xx
#python security-check-2.py     -f      nodes-4.json
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
	message['From'] = 'chxxxx@gmail.com'
	message['To'] = 'sxxxxx@gmail.com'
	message.preamble = 'Multipart message.\n'
	message.attach(MIMEText('status of service'))	
	part = MIMEApplication(log_data)
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % log_file)
	message.attach(part)
	client = boto3.client('ses')
	response = client.send_raw_email (Source='chxxxxxx@gmail.com',Destinations=['sxxxxx@gmail.com'],RawMessage={'Data': message.as_string()})
def json_string(file):
	foo = open("%s"%file,'r')
	s = ""
	for line in foo:
		s+=str(line)
	json_data = json.loads(s)
	foo.close()
	return json_data
def execute(pem,user,ip):
		print ip
		cmd1 = "scp -i %s /home/controller/Desktop/logs/check.sh  %s@%s:/tmp"%(pem,user,ip)
    		p = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
    		cmd2 = "ssh -i %s  %s@%s 'bash /tmp/check.sh'"%(pem,user,ip)
		p = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)	
		out, err = p.communicate()
		if out == "":
			out = "NA"
		print out
		return out
def outl(us,tp,prod_ip,prod_ss):
		outp = ""
		if ("additional hardrive present" in us) and ("critical" not in us):
			outp += "%s,%s,%s,"%(prod_ip,tp,prod_ss)
			bhf = us.split("\n")[0]
			hf = bhf.split(" ")[1]
			host = hf.split(":")[1]
			ta = us.split("\n")[2]
			tb = us.split("\n")[3]
			tc =us.split("\n")[4]
			lbs = ta.split(" ")[3]
			if lbs != "/opt/data":
				lbs = "NA"
			else:
				pass
			outp+="%s,YES,%s,%s,%s\n"%(host,lbs,tb,tc)
			return outp
		else:
			fun = us.split("\n")
			hf = fun[0].split(" ")[1]
			host = hf.split(":")[1]
			outp += "%s,%s,%s,%s,NO,NA,NA,NA\n"%(prod_ip,tp,prod_ss,host)
		return outp
def	security_check_f(json_file):
 with open("out.csv","a+") as temp:
 	temp.write("IP,Deployment Name, SSID , Node ID, Additional disk available , Logs being stored in /opt/data/ , Solr log path ,ZK logs path\n")
	js = json_string(json_file)
	prod_u=js["prod"][0].split(":")[1]
	prod_k=js["prod"][1].split(":")[1]
	if len(js["prod"]) == 3:
		tp = "prod"
		prod_ss = js["prod"][2].split(":")[0]
		prod_ip = js["prod"][2].split(":")[1]
		us = execute(prod_k,prod_u,prod_ip)
		temp.write(outl(us,tp,prod_ip,prod_ss))
	elif len(js["prod"]) > 3:
		for i in range (3,len(js["prod"])):
			tp="prod"
			prod_ss = js["prod"][i-1].split(":")[0]
			prod_ip = js["prod"][i-1].split(":")[1]
			us = execute(prod_k,prod_u,prod_ip)
			temp.write(outl(us,tp,prod_ip,prod_ss))
	else:
		print ("no ips were found .")
	qa_u=js["qa"][0].split(":")[1]
	qa_k=js["qa"][1].split(":")[1]
	if len(js["qa"]) == 3:
		tp = "qa"
		qa_ss = js["qa"][2].split(":")[0]
		qa_ip = js["qa"][2].split(":")[1]
		us = execute(qa_k,qa_u,qa_ip)
		temp.write(outl(us,tp,qa_ip,qa_ss))
	elif len(js["qa"]) > 3:
		for i in range (3,len(js["qa"])):
			tp="qa"
			qa_ss = js["qa"][2].split(":")[0]
			qa_ip = js["qa"][2].split(":")[1]
			us = execute(qa_k,qa_u,qa_ip)
			temp.write(outl(us,tp,qa_ip,qa_ss))
	else:
		print ("no ips were found .")
 now = dt.now()
 fname = "%d-%d-%d-%d-%d-%d.csv"%(now.year,now.month,now.day,now.hour,now.minute,now.second)
 with open("out.csv","r") as foo:
	csv_read = csv.reader(foo)
	with open("%s"%str(fname),"w+") as new:
		csv_write = csv.writer(new,delimiter=',')
		for line in csv_read:
			csv_write.writerow(line)
 sendLogFileEmail("%s"%str(fname),open("output.csv").read()) 
 p = subprocess.Popen("rm out.csv", stdout=subprocess.PIPE, shell=True)
def	security_check(ip, user, pem):
	if "@" in ip:
		user = ip.split("@")[0]
		ip= ip.split("@")[1]
	execute(pem,user,ip)
if __name__ == '__main__':
	import argparse
	parser = argparse.ArgumentParser(description='Receive the input file directory.')
	parser.add_argument("-f", nargs="?", metavar='N', type=str, help="file contains eips which are need to be released")
	parser.add_argument("-n",help="security check on single node")
	parser.add_argument("-u", type=str, help="user to login")
	parser.add_argument("-i", type=str, help="path to .pem file")
	args = parser.parse_args()
	json_file, ip = None, None
	if (args.n is not None ) and (args.u is not None ) and (args.i is not None ) and (args.f is None ):
		ip	 = args.n
		user = args.u
		pem	= args.i
		execute(pem,user,ip)
	elif (args.n is None ) and (args.u is None ) and (args.i is None ) and (args.f is not None ):
		security_check_f(args.f)
	else:
		print "Unspecified Error"
