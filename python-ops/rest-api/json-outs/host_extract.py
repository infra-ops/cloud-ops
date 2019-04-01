import csv
import json,socket
import argparse
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth



fich = open("env.json","r")
#headers = {'Content-Type': 'application/json','Authorization':'Bearer S8qGItb7fe1VwFjX8yX3aH96BXHWdK' }
tempd = json.load(fich)
prod = tempd["prod"]
stage = tempd["stage"]

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

parser = argparse.ArgumentParser()
parser.add_argument("-e")
args=parser.parse_args()
if args.e == "prod":
	headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%prod[1] }
	r = requests.get('%s/api/v2/hosts'%prod[0], headers=headers)
	data = json.loads(r.text)
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
elif args.e == "stage":
        headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%stage[1] }
        r = requests.get('%s/api/v2/hosts'%stage[0], headers=headers)
        data = json.loads(r.text)
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
else:
	print "missing arguments"
