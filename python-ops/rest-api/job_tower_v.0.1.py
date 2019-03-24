import csv
import json,socket
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth


url = 'http://localhost/api/v2/jobs'
r = requests.get(url, auth=HTTPBasicAuth('admin', 'password'))
data = json.loads(r.text)
#print data
i=0
while True:
	try:
		if data["results"][i]["status"]=="successful":
			name= data["results"][i]["name"]
			jobt= data["results"][i]["job_type"]
			proj = data["results"][i]["project"]
			cred = data["results"][i]["credential"]
			print name
			print jobt
			print proj
			print cred
			i=i+1
		else:
			i=i+1

	except:
		break
