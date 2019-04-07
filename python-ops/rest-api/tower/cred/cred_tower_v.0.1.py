import csv
import json,socket
import requests
import re,yaml
import argparse
from datetime import datetime
from requests.auth import HTTPBasicAuth


def cred(id):
	url1 = 'http://localhost/api/v2/credentials/%s/'%id
	r1 = requests.get(url1, auth=HTTPBasicAuth('admin', 'password'))
	data1 = json.loads(r1.text)
	username = data1["inputs"]["username"]
	writer.writerow([username])
	print username
out = open("report1.csv","w+")
writer = csv.writer(out)
parser = argparse.ArgumentParser()
parser.add_argument("-c")
args = parser.parse_args()
if (args.c is not None):
	ff = open(args.c,"r")
	dat = yaml.load(ff)
	ids=dat[0]["cred"]
	writer.writerow(["username"])
	print "username"
	for id in ids:
		cred(id)
else:
	print "missing arguments"
