#python key-5.py -a 692683949874-compute@developer.gserviceaccount.com -k connector-2-250114-d261c3498843.json -e stage -l http://192.168.10.117 -t 1K7eLFJL1XNU0nglxaqd7gk3DNTCGf -c gcp-test-1 -u test-sa-9@connector-2-250114.iam.gserviceaccount.com -p connector-2-250114 -i 5

#export GOOGLE_APPLICATION_CREDENTIALS="/home/nik/Desktop/git-repo/python-git/python-ops/rest-api/tower/jobs/sa/sa-env/connector-2-250114-d261c3498843.json"
#export http_proxy=""


import argparse
import os
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




# [START iam_create_key]
def create_key(service_account_email,keyfile,envi,link,token,cred_name,user,proj,idd):
    """Creates a key for a service account."""

    

    credentials = service_account.Credentials.from_service_account_file(keyfile)
    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)
    service = googleapiclient.discovery.build(
        'iam', 'v1', credentials=credentials)
    
    body = {
            # TODO: Add desired entries to the request body.
            "keyAlgorithm": "KEY_ALG_RSA_2048",
            "privateKeyType": "TYPE_GOOGLE_CREDENTIALS_FILE"
    }


    key = service.projects().serviceAccounts().keys().create(
        name='projects/-/serviceAccounts/' + service_account_email, body=body
        ).execute()

    my_json = base64.b64decode(key['privateKeyData']).decode('utf8')
    k = json.loads(my_json)
    with open("cred.json", 'w') as f:
        json.dump(k, f, indent=2)
    print('Created key: ' + key['name'])
    ansible_cred(proj,cred_name,envi,idd,link,token,user)
   
def ansible_cred(proj,name,envi,idd,url,toke,user):
    creds = open("cred.json","r")
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
    r1 = requests.put(u1,headers=headers,json=data, verify=False)
    data=json.loads(r1.text)
    dat = (str(url),str(toke),str(data))
    print(dat)










parser = argparse.ArgumentParser()

parser.add_argument("-e","--env", required=True)
parser.add_argument("-l","--link", required=True)
parser.add_argument("-t","--token", required=True)
parser.add_argument("-a","--email", help="email id in GCP", required=True)
parser.add_argument("-k","--keyname", help="keyfile for authentication", required=True)
parser.add_argument("-c","--name", required=True)
parser.add_argument("-u","--user", required=True)
parser.add_argument("-p","--project", help="project id in GCP", required=True)
parser.add_argument("-i","--id", required=True)




args = parser.parse_args()




#print (args.project)
#create_key(args.email,args.keyname)
create_key(args.email,args.keyname,args.env,args.link,args.token,args.name,args.user,args.project,args.id)
