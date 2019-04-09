import csv
import json,socket
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth
#print data
status=[]
page=1
while True:
	try:

			url = 'http://localhost/api/v2/jobs?status=successful&page=%s&page_size=100'%page
			r = requests.get(url, auth=HTTPBasicAuth('admin', 'password'),verify=False)
			data = json.loads(r.text)
			num = len(data["results"])
			if data["next"]=="null":
				for i in range(0,num):
					id=data["results"][i]["id"]
                			u2 = 'http://localhost/api/v2/jobs/%s/cancel/'%id
                			r2 = requests.post(u2, auth=HTTPBasicAuth('admin', 'password'),headers={ 'Content-Type' : 'application/json'},verify=False)
                			print "%s job deleted %s"%(id,r2.status_code)
				break
                        else:
                                for i in range(0,num):
					id=data["results"][i]["id"]
                                        u2 = 'http://localhost/api/v2/jobs/%s/cancel/'%id
                                        r2 = requests.post(u2, auth=HTTPBasicAuth('admin', 'password'),headers={ 'Content-Type' : 'application/json'},verify=False)
                                        print "%s job deleted %s"%(id,r2.status_code)
				page=page+1

	except:
		break
