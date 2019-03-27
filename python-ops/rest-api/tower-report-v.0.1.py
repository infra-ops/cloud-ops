import csv
import json,socket
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth

#page is incremental value..it can be enahnced till 1000 pages

#page=0
#u1 = 'http://localhost/api/v2/job/?launch_type=manual&job_type=run&started_gt=2019-03-10T15:06:07.160038Z&started_lt=2019-03-25T15:06:07.160038Z + page + "&page_size=100"'
u1 = 'http://localhost/api/v2/jobs/'
r = requests.get(u1, auth=HTTPBasicAuth('admin', 'password'))
data = json.loads(r.text)
i=0
ff = open("report3.csv","w+")
writing = csv.writer(ff)
writing.writerow(["GB\tGF\tPROJECT_NAME","JOB_NAME","STATUS","LAUNCHER"])
print "GB\tGF\tPROJECT_NAME\tJOB_NAME\tSTATUS\tLAUNCHER"
while True:
	try:
	       temp = data["results"][i]["name"]
               proj=data["results"][i]["project"]
               sta = data["results"][i]["status"]
               #fetch project name
               u2 = "http://localhost/api/v2/projects/%s/?page_size=100"%str(proj)
               r2 = requests.get(u2, auth=HTTPBasicAuth('admin', 'password'))
               data2 = json.loads(r2.text)
               pname = data2["name"]

               #fetch launcher name
               page_ur=data["results"][i]["related"]["created_by"]
               u3 = "http://localhost%s"%str(page_ur)
               r3 = requests.get(u3, auth=HTTPBasicAuth('admin', 'password'))
               data3 = json.loads(r3.text)
               uname = data3["username"]
               print "%s\t%s\t%s\t%s"%(pname,temp,sta,uname)
	       writing.writerow([pname,temp,sta,uname])
               i=i+1
	except Exception as e:
		break
