import csv
import json,socket
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth


url = 'http://localhost/api/v2/jobs'
r = requests.get(url, auth=HTTPBasicAuth('admin', 'password'))
data = json.loads(r.text)
ff = open("report.csv","w+")
writer = csv.writer(ff)
writer.writerow(["name","job_type","project","status","credential"])
print "name\tjob_type\tproject\tstatus\tcredential"
i=0
while True:
	try:
		if data["results"][i]["status"]=="successful":
			name= data["results"][i]["name"]
			jobt= data["results"][i]["job_type"]
			proj = data["results"][i]["project"]
			cred = data["results"][i]["credential"]
			writer.writerow([name,jobt,proj,data["results"][i]["status"],cred])
			print "%s\t%s\t%s\t%s\t%s"%(name,jobt,proj,data["results"][i]["status"],cred)
			i=i+1
		else:
			i=i+1

	except:
		break
