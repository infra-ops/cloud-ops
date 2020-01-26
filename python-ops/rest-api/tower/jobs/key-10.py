import argparse
import os,subprocess
from google.oauth2 import service_account
import googleapiclient.discovery
import base64
import json,requests
from googleapiclient.errors import HttpError
from google.oauth2 import service_account
from requests.auth import HTTPBasicAuth
from pprint import pprint
from oauth2client.client import GoogleCredentials
requests.packages.urllib3.disable_warnings()




   
def ansible_cred():
    credf = open("/opt/apps/cred.json","r")
    tmp = json.load(credf)
    key = tmp["private_key"]
    print key
    data = {
            "name": "gcp-test-1",
            "description": "",
            "organization": 1,
            "credential_type": 10,
            "inputs":  {
                "username": "test-sa-8@connector-2-250114.iam.gserviceaccount.com",
                "project":  "connector-2-250114 -i",
                "ssh_key_data": key,
                }
            }
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer 1K7eLFJL1XNU0nglxaqd7gk3DNTCGf'}
    u1 = 'http://192.168.10.117/api/v2/credentials/5/'
    r1 = requests.put(u1,headers=headers,json=data, verify=True)
    data=json.loads(r1.text)
    print(data)


ansible_cred()

#print (args.project)
#create_key(args.email,args.keyname)
#ansible_cred(args.env,args.link,args.token,args.cred_name,args.user_name,args.project,args.id)


