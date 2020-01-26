#python key-8.py -a  connector-svc-05@connector-2-250245.iam.gserviceaccount.com -k connector-2-245-40701f315643.json /
-i inv.yml -j copy-3.yml -e stage -l http://192.168.10.117 -t 1K7eLFJL1XNU0nglxaqd7gk3DNTCGf 
/ -c gcp-test-1 -u test-sa-12@connector-2-240114.iam.gserviceaccount.com -p connector-2-245 -o 5

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
def create_key(service_account_email,keyfile,first_yml,second_yml,arg1,arg2,arg3,arg4,arg5,arg6,arg7):
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

    execute(first_yml,second_yml,arg1,arg2,arg3,arg4,arg5,arg6,arg7)


def execute(f_yml,s_yml,arg1,arg2,arg3,arg4,arg5,arg6,arg7):
        old = open(s_yml,"r")
        alls = old.readlines()
        old.close()
	final = []
	for line in alls:
		if "shell" in line:
			try:
				line = line.split(".")[0]
				final.append(line)
			except:
				final.append(line)
		else:
			final.append(line)
       	with open(s_yml,"w+") as new:
		for line in final:
			if "shell" in line:
				line = str(line).replace("\n","") + ".py -e %s -l %s -t %s -c %s -u %s -p %s -o %s\n"%(arg1,arg2,arg3,arg4,arg5,arg6,arg7)
				new.write("%s\n"%line.replace("\n",""))
			else:
				new.write("%s\n"%line.replace("\n",""))
	cmd2 = "ansible-playbook -i %s %s"%(f_yml,s_yml)
	p=subprocess.Popen("%s"%(cmd2), stdout=subprocess.PIPE, shell=True)
        out,err= p.communicate()
        print out



parser = argparse.ArgumentParser()
parser.add_argument("-a","--email", help="email id in GCP", required=True)
parser.add_argument("-k","--keyname", help="keyfile for authentication", required=True)
parser.add_argument("-i", required=True)
parser.add_argument("-j", required=True)
parser.add_argument("-e", required=True)
parser.add_argument("-l", required=True)
parser.add_argument("-t", required=True)
parser.add_argument("-c", required=True)
parser.add_argument("-u", required=True)
parser.add_argument("-p", required=True)
parser.add_argument("-o", required=True)
args = parser.parse_args()
#print (args.project)
create_key(args.email,args.keyname,args.i,args.j,args.e,args.l,args.t,args.c,args.u,args.p,args.o)

