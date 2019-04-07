import csv
import json,socket
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth


headers = {'Content-Type': 'application/json','Authorization':'Bearer S8qGItb7fe1VwFjX8yX3aH96BXHWdK' }

def work(data):
	i=0
	while True:
		try:
       	               temp = data["results"][i]["name"]
	               proj=data["results"][i]["project"]
	               sta = data["results"][i]["status"]
	               #fetch project name
	               u2 = "http://localhost/api/v2/projects/%s/?page_size=100"%str(proj)
                       r2 = requests.get(u2,headers=headers,verify=False)
	               data2 = json.loads(r2.text)
	               pname = data2["name"]
	               gb=pname.split("_")[0]
	               gf=pname.split("_")[1]
	               #fetch launcher name
	               page_ur=data["results"][i]["related"]["created_by"]
	               u3 = "http://localhost%s"%str(page_ur)
		       r3 = requests.get(u3,headers=headers,verify=False)
	               data3 = json.loads(r3.text)
	               uname = data3["username"]
	               print "%s\t%s\t%s\t%s\t%s\t%s"%(gb,gf,pname,temp,sta,uname)
	               writing.writerow([pname,temp,sta,uname])
	               i=i+1
		except Exception as e:
			break
ff = open("report3.csv","w+")
writing = csv.writer(ff)
writing.writerow(["GB\tGF\tPROJECT_NAME","JOB_NAME","STATUS","LAUNCHER"])
print "GB\tGF\tPROJECT_NAME\tJOB_NAME\tSTATUS\tLAUNCHER"
page = 1
while True:
	try:
	        u1 = 'http://localhost/api/v2/jobs/?job_type=run&launch_type=manual&page=%s&started__gt=2019-03-20T00:00&started__lt=2019-03-26T00:00&page_size=100'%page  
                r1 = requests.get(u1,headers=headers,verify=False)
	        data=json.loads(r1.text)
		if data["next"]=="null":
			work(data)
			break
		else:
			work(data)
			page=page+1
	except:
		break
