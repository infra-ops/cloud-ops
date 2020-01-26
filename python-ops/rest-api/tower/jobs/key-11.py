#python key-8.py -a  connector-04@connector-2-245.iam.gserviceaccount.com -k connector-2-245-40701f31aa23.json \
#-i inv.yml -j copy-2.yml



import argparse
import os
import subprocess
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
def create_key(service_account_email,keyfile,first_yml,second_yml):
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

    execute(first_yml,second_yml)


def execute(f_yml,s_yml):
	cmd2 = "ansible-playbook -i %s %s"%(f_yml,s_yml)
	p=subprocess.Popen("%s"%(cmd2), stdout=subprocess.PIPE, shell=True)
        out,err= p.communicate()
        print out



parser = argparse.ArgumentParser()
parser.add_argument("-a","--email", help="email id in GCP", required=True)
parser.add_argument("-k","--keyname", help="keyfile for authentication", required=True)
parser.add_argument("-i", required=True)
parser.add_argument("-j", required=True)

args = parser.parse_args()
#print (args.project)
create_key(args.email,args.keyname,args.i,args.j)
