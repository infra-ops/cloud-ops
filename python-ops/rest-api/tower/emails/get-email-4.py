import csv
import json,socket
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth
#print data
emails=[]
page=1
while True:
	try:

			url = 'http://localhost/api/v2/users/?page=%s&page_size=100'%page
			r = requests.get(url, auth=HTTPBasicAuth('admin', 'password'))
			data = json.loads(r.text)
			num = len(data["results"])
                        if data["next"]=="null":
				for i in range(0,num):
                        		email = data["results"][i]["email"]
					emails.append(email)
				break
                        else:
	        		for i in range(0,num):
	                        	email = data["results"][i]["email"]
        	                        emails.append(email)
				page=page+1

	except:
		break

"""
for mail in emails:
	print mail
"""

for mail in emails:
    #mails = '' + str(mail) + ','
    print(mail + ",")


