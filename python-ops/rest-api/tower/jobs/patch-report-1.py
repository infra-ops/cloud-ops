import argparse,json
import csv
import requests,subprocess
from bs4 import BeautifulSoup
from email import Encoders
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText

def mail(report):
         msg = MIMEMultipart()
	 msg["From"] = "me@example.com"
	 msg["To"] = "sudipta1436@gmail.com"
	 msg["Subject"] = "Report Ansible."
	 text="KINDLY CLICK ON BELOW MENTIONED LINK FOR PATCH UPDATE\nhttp://localhost/api"
	 part1 = MIMEText(text, 'plain')
         part = MIMEBase('application', "octet-stream")
       	 part.set_payload(open(report, "rb").read())
	 Encoders.encode_base64(part)
         part.add_header('Content-Disposition', 'attachment', filename=report)
         msg.attach(part)
	 msg.attach(part1)
         p =subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
	 p.communicate(msg.as_string())
	 print "done"
def clean(resp):
	hosts=[]
	temp=[]
        for i in resp:
                if "TASK [check for update] ********************************************************" in i:
                        del resp[0:resp.index(i)+1]
                        break
        for i in resp:
                if "PLAY RECAP *********************************************************************" in i:
                        del resp[resp.index(i):len(resp)-1]
                        break
	for i in resp:
		if "TASK [print out] ***************************************************************" in i:
			temp = resp[0:resp.index(i)-1]
			del resp[0:resp.index(i)+1]
			for j in temp:
                        	j=j.replace('<span class="ansi32">ok: [',"")
                        	j=j.replace("]</span>","")
                        	hosts.append(j)
			break
        one=[]
	fo = open("patch-update-available.csv","w+")
	writer=csv.writer(fo)
	writer.writerow(["HOSTNAMES","PACKAGES NAMES"])
        for j in resp:
                j=j.replace('<span class="ansi32">        ',"")
                j=j.replace(', </span>',"")
		j=j.replace('<span class="ansi32">',"")
		j=j.replace('</span>',"")
                one.append(j)
	for host in hosts:
		modules=[]
		ip = 'ok: [%s] =&gt; {'%host
		for k in one:
			if k == ip:
				for j in range(one.index(k),len(one)):
					if "}" in one[j]:
						break
					else:
						modules.append(one[j])
		del modules[0]
		try:
			del modules[len(modules)-1]
			del modules[0]
		except:
			pass
		try:
                        writer.writerow([host,modules[0].replace('"','')])
                        del modules[0]
                except:
                        writer.writerow([host,""])
                for q in modules:
                        writer.writerow(["",q.replace('"',"")])

def work(token,url):
	with requests.session() as o:
		headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%token }
		first= o.get("%s/api/v2/job_templates/28/"%url,headers=headers)
		data = json.loads(first.text)
		last_job= data["related"]["last_job"]
		second = o.get("%s%s"%(url,last_job),headers=headers)
		data= json.loads(second.text)
		status=data["status"]
		if status == "successful":
			stdoout=data["related"]["stdout"]
			third = o.get("%s%s"%(url,stdoout),headers=headers)
			resp = third.text
			resp = resp.split("\n")
			clean(resp)
			mail("patch-update-available.csv")
		else:
			quit()
parser = argparse.ArgumentParser()
parser.add_argument("-e")
args = parser.parse_args()
if args.e == "prod":
	fo = open("env.json","r")
	data=json.load(fo)
	fo.close()
	url = data["prod"][0]
	token= data["prod"][1]
	work(token,url)
elif args.e == "stage":
        fo = open("env.json","r")
        data=json.load(fo)
        fo.close()
        url = data["stage"][0]
        token= data["stage"][1]
        work(token,url)
else:
	print "missing argument !"
	quit()

