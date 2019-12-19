#/usr/bin/python3 sa-18.py -e stage -s sample-sa-1 -d dp-1 -c 1 -k key-12.json 
#

#functionality of code is below mentioned

#1. service-accounts and  display-name will be provided as args  -s sample-sa-1 -d dp-1 which will create service account and display name
#2. gcloud command will create key-16.json which will be passed as args -k key-16.json
#3. private key content will be fetched from key-16.json and parsed to json body
#4. post call will be executed with this json body
#5. cid will be passed as args -c 1
#6. restapi and url will be taken from env-2.json
#problem of this code is everything is arranged but somethings are not finctional which need to be fixed
#execute function() works fine but there is issue in post function()

import subprocess
import requests
import re
import yaml
import datetime
import requests,argparse
from requests.auth import HTTPBasicAuth
import json
requests.packages.urllib3.disable_warnings()

print(str(datetime.datetime.now().time()) + " Script started")
print("")
arged = False
stageenv = {}


def execute():
    if arged == True:
        cmd1 = f"gcloud iam service-accounts create {stageenv['service-accounts']} --display-name {stageenv['display-name']}"
        cmd2 = f"gcloud iam service-accounts keys create --iam-account {stageenv['test-account']}@connector-2-250114.iam.gserviceaccount.com {stageenv['key-name']}"
        
        cmd3 = f'grep -o "\-.*BEGIN.*" {stageenv["key-name"]}'
    else:
        cmd1 = f"gcloud iam service-accounts create {stageenv['service-accounts']} --display-name {stageenv['display-name']}"
        cmd2 = f"gcloud iam service-accounts keys create --iam-account {stageenv['test-account']}@connector-2-250114.iam.gserviceaccount.com {stageenv['key-name']}"
        
        cmd3 = f'grep -o "\-.*BEGIN.*" {stageenv["key-name"]}'
    print(cmd1)
    print(cmd2)
    print(cmd3)
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, shell=True)
    out, err = p1.communicate()
    if out == "":
        out = "NA"
    print(out)
    p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)
    out2, err = p2.communicate()
    if out2 == "":
        out2 = "NA"
    print(out2)
    # return out, out2
   
    p3 = subprocess.Popen(cmd3, stdout=subprocess.PIPE, shell=True)
    out3, err = p3.communicate()
    if out3 == "":
        out3 = "NA"
    print(out3)
    return out, out2, out3
    

def post(stage, env):
    data = {
            "name": "gcp-test-1",
            "description": "",
            "organization": 1,
            "credential_type": 10,
            "inputs":  {
                "username": "itest-sa-1@connector-2-250114.iam.gserviceaccount.com",
                "project":  "connector-2-250114-3",
                "ssh_key_data": f"[ grep -o '\-.*BEGIN.*' {env['key-name']} ]",
                }
            }
    url=stage[0] 
    toke=stage[1]
    
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%toke}
    u1 = f'{url}/api/v2/credentials/{env["cid"]}'
    r1 = requests.post(u1,headers=headers,json=data, verify=False)
    data=json.loads(r1.text)
    dat = (str(url),str(toke),str(data))
    print (dat)

fich =  open('env-2.json','r')
tempd = json.load(fich)
prod = tempd["prod"]
stage = tempd["stage"]

parser = argparse.ArgumentParser()
parser.add_argument("-e")
parser.add_argument("-s")
parser.add_argument("-d")
parser.add_argument("-t")
parser.add_argument("-c")
parser.add_argument("-k")
args=parser.parse_args()

stageenv['service-accounts'] = args.s
stageenv['display-name'] = args.d
stageenv['test-account'] = args.t
stageenv['cid'] = args.c
stageenv['key-name'] = args.k


execute()

if (args.e == "stage") and (args.s is not None) and (args.d is not None) and (args.t is not None) and (args.c is not None) and (args.k is not None):
        try:
            ptrg = open(args.k, 'r')
            putargtmp = ptrg.read()
        except Exception as e:
            print(e)
        post(stage, stageenv)

else:
   print("missing arguments")


#post("http://192.168.10.117","1")
#post()
print("")
print(str(datetime.datetime.now().time()) + " Script ended")

