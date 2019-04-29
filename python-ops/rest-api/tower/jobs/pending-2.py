
import csv
import json,socket
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth

def work(data):
                headers = { 'Content-Type' : 'application/json' }
                num = len(data["results"])
		for i in range(0,num):
			id = data["results"][i]["id"]
                 	u2 = 'http://localhost/api/v2/jobs/%s/cancel/'%str(id) 
                 	r2 = requests.post(u2, auth=HTTPBasicAuth('admin', 'password'),headers=headers,verify=False) 
                 	print "%s job has been deleted"%(id)
page = 1
while True:
           try:
                   u1 = 'http://localhost/api/v2/jobs/?status=failed&page=%s&page_size=100'%page
                   r1 = requests.get(u1, auth=HTTPBasicAuth('admin', 'password'),verify=False) 
                   data=json.loads(r1.text)
		   if data["next"]=="null":
                   	work(data)
                   	break
                   else:
                   	work(data)
                   	page=page+1
           except:
                   break

