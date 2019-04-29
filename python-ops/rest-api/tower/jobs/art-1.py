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
    data=str(l).replace("{","").replace("}","").replace("u","").replace("'","")
    print data



"""

{'playbook_uuid': u'ac9090d6-9a41-497c-8850-a28cd148897e', u'pid': 923, u'playbook': u'helo.yml'}
{u'play_pattern': u'dev', u'play': u'dev', u'pid': 923, u'play_uuid': u'0242ac11-0006-8678-2752-000000000006', u'playbook_uuid': u'ac9090d6-9a41-497c-8850-a28cd148897e', u'playbook': u'helo.yml', u'error': True}
{u'play_pattern': u'dev', u'play': u'dev', u'name': u'dev', u'pattern': u'dev', u'pid': 923, u'play_uuid': u'0242ac11-0006-8678-2752-000000000006', u'playbook_uuid': u'ac9090d6-9a41-497c-8850-a28cd148897e', u'playbook': u'helo.yml'}


"""
