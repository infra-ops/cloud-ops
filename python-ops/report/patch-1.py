import subprocess
import argparse
from datetime import datetime
import pandas as pd
import re
import  json
from  bson.json_util  import  dumps
import plotly as py
from email import Encoders
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText

def copy():
        p = subprocess.Popen("ansible-playbook -i ./inv3.sh copy.yml",shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()
def mail():
         msg = MIMEMultipart()
         msg["From"] = "me@example.com"
         msg["To"] = "sudipta1436@gmail.com"
         msg["Subject"] = "Report Ansible."
         text="""Kindly click on below mentioned url to check patch updates\nhttp://xxxxxxxxxxx/patch/"""
         msg.attach(MIMEText(text))
         p =subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
         p.communicate(msg.as_string())



def cmds(ip,usr,pwd):
        #this function will initialize all the commands and give them to run function for execution and return the output as well
        ip=str(ip)
        ip2 = "sshpass -p "+pwd+" ssh "+usr+"@"+ip+" "+"sudo yum check-update"
        p = subprocess.Popen(ip2 ,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        out, err=p.communicate()
        return out
def json_read_file(json_file):
#this function will get all hosts ,usernames and passwords and pass them for execution , after the execution it'll print the output and write to csv file
        f = open(json_file,"r+")
        datax = json.load(f)
        keyz = datax.keys()
        status_machine=[]
	j=0
        for i in range(0,len(keyz)):
                try:
                                hosts = datax[keyz[i]]["hosts"]
                                user = datax[keyz[i]]["vars"]["ansible_ssh_user"]
                                psw = datax[keyz[i]]["vars"]["ansible_ssh_pass"]
				for ip in hosts:
					filex = open("%s.html"%ip,"w+")
					new=[]
					final=[]
                                        data=cmds(ip,user,psw)
					data=data.split("\n")
					del data[:2]
					filex.write("<html><table border='1'><tr><th>Package Name</th><th>Versions</th><th>Repo</th></tr>")
					for i in data:
						i=i.split(" ")
						new.append(i)
					for lo in new:
							lo=filter(None, lo)
							final.append(lo)
					del final[len(final)-1]
					for fl in range(0,len(final)-1):
						try:
							if len(final[fl]) != 3:
								final[fl]=final[fl]+final[fl+1]
								del final[fl+1]
						except:
							break
					for fl in range(0,len(final)-1):
							filex.write("<tr>\n")
							for it in final[fl]:
								filex.write("<td>%s</td>\n"%it)
							filex.write("</tr>")
					j=j+1
					print ip
					filex.close()
                                        continue
                except Exception as e:
                                continue

if __name__ == '__main__':
#here will be arguments control and initialisation
        parser = argparse.ArgumentParser()
        parser.add_argument("-i")
        args = parser.parse_args()
        if args.i is not None:
		startTime = datetime.now()
		print "script started at: %s"%startTime
                json_read_file(args.i)
		copy()
		mail()
		print "script ended at: %s"%datetime.now()
        else:
                print "Missing arguments"
