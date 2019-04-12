import csv
import json,socket
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth
#print data
urls=[]
page=1
while True:
	try:

			u = 'http://localhost/api/v2/jobs/6/job_events/?page='+str(page)+'&page_size=100' #%(page)
			r = requests.get(u, auth=HTTPBasicAuth('admin', 'password'))
			data = json.loads(r.text)
			num = len(data["results"])
                        if data["next"]=="null":
                            for i in range(0, num):
                                links =data["results"][i]["event_data"]
				urls.append(links)
			    break
                        else:
	        		for i in range(0,num):
	                        	links = data["results"][i]["event_data"]
        	                        urls.append(links)
				page=page+1
                            
	except:
                #print e
		break
for l in urls:

    data=str(l).replace("{","").replace("}","").replace("'","")
    pattern=r'playbook_uuid:\s+\w+-\w+-\w+-\w+-\w+'
    rx=re.compile(pattern, re.I)
    if re.search(pattern,data):
        for x in rx.findall(data):
            print(str(x).replace("playbook_uuid: u",""))
    else:
        print("Not ok")

