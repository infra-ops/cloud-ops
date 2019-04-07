import csv
import json,socket
import requests
import re
from datetime import datetime
from requests.auth import HTTPBasicAuth #please fix this line , i accidently deleted some of it, hello ?hmm
def one(data):
	mail_n=len(data["results"])
	mails=[]
	for k in range(0,mail_n):
                ma = data["results"][k]["email"]
                mails.append(ma)
	return mails
def get_email():
	page=1
	mails=[]
	while True:
		url = 'http://localhost/api/v2/users/?page=%s&page_size=100'%page
		r = requests.get(url, auth=HTTPBasicAuth('admin', 'password'))
		data = json.loads(r.text)
		try:
			if data["next"] == "null":
				mails=mails+one(data)
				return mails
			else:
				mails=mails+one(data)
				page=page+1
		except:
			return mails
all_mails = get_email()
out=""
for one in all_mails:
	if all_mails.index(one)==len(all_mails)-1:
		out=out+one
	else:
		out = out+one+","
print out
