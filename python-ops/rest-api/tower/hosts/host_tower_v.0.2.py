import csv
import json,socket
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth


url = 'http://localhost/api/v2/hosts'
r = requests.get(url, auth=HTTPBasicAuth('admin', 'password'))
data = json.loads(r.text)
def hosts(data):
    ips=[]
    i=0
    while True:
        	try:
	        	ip=data["results"][i]["name"]
		        ips.append(ip)
		        i=i+1
	        except:
		               break
    return ips

hosts= hosts(data)
current_time=datetime.now()
date_format=current_time.strftime("%Y-%m-%d-%H-%M-%S")
namefile="%s.csv" %(date_format)
with open(namefile, "a") as fl:
	opt=csv.writer(fl, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	opt.writerow(["IP"])
	for row in hosts:
    		print row
		opt.writerow([row])
