import csv
import json,socket
import requests
import re,yaml
import argparse
from datetime import datetime
from requests.auth import HTTPBasicAuth


def proj(id):
	url1 = 'http://localhost/api/v2/projects/%s/'%id
	r1 = requests.get(url1, auth=HTTPBasicAuth('admin', 'password'))
	data1 = json.loads(r1.text)
	name = data1["name"]
	url = data1["scm_url"]
	writer.writerow([name,url])
	print "%s\t%s"%(name,url)
out = open("report.csv","w+")
writer = csv.writer(out)
parser = argparse.ArgumentParser()
parser.add_argument("-p")
args = parser.parse_args()
if (args.p is not None):
	ff = open(args.p,"r")
	dat = yaml.load(ff)
	ids=dat[0]["proj"]
	writer.writerow(["name","scm_url"])
	print "name\tscm_url"
	for id in ids:
		proj(id)
else:
	print "missing arguments"
