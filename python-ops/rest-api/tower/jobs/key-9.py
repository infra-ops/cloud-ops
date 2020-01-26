#python key-9.py -e stage -l http://192.168.10.117 -t 1K7eLFJL1XNU0nglxaqd7gk3DNTCGf -c \
#gcp-test-1 -u test-sa-9@connector-2-250114.iam.gserviceaccount.com -p connector-2-250114 -o 5



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




   
def ansible_cred(proj,name,envi,idd,url,toke,user):
    creds = open("/opt/apps/cred.json","r")
    tmp = json.load(creds)
    key = tmp["private_key"]
    print key
    data = {
            "name": name,
            "description": "",
            "organization": 1,
            "credential_type": 10,
            "inputs":  {
                "username": user,
                "project":  proj,
                "ssh_key_data": key,
                }
            }
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%toke}
    u1 = '%s/api/v2/credentials/%s/'%(url,idd)
    r1 = requests.put(u1,headers=headers,json=data, verify=True)
    data=json.loads(r1.text)
    dat = (str(url),str(toke),str(data))
    print(dat)







parser = argparse.ArgumentParser()

parser.add_argument("-e","--env", required=True)
parser.add_argument("-l","--link", required=True)
parser.add_argument("-t","--token", required=True)
#parser.add_argument("-a","--email", help="email id in GCP", required=True)
#parser.add_argument("-k","--keyname", help="keyfile for authentication", required=True)
parser.add_argument("-c","--name", required=True)
parser.add_argument("-u","--user", required=True)
parser.add_argument("-p","--project", help="project id in GCP", required=True)
parser.add_argument("-o","--id", required=True)




args = parser.parse_args()


#there is no ansible cred here bro...old key-9 was getting copied here which i have blocked now..

#print (args.project)
#create_key(args.email,args.keyname)
ansible_cred(args.project,args.name,args.env,args.id,args.link,args.token,args.user)
#proj,name,envi,idd,url,toke,user
