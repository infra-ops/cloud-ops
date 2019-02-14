import csv
import json
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth

 
url = 'http://localhost/api/v2/hosts'
 
r = requests.get(url, auth=HTTPBasicAuth('admin', 'password'))
 
data = str(r.json())
 
rst=re.compile(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', re.U)

current_time=datetime.now()
date_format=current_time.strftime("%Y-%m-%d-%H-%M-%S")
 
namefile="%s.csv" %(date_format)


with open(namefile, "a") as fl:
	opt=csv.writer(fl, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	opt.writerow(["IP"])
	for row in rst.findall(data):
    		print(row)
		opt.writerow([row])
