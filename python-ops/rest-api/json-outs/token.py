import requests,argparse
from requests.auth import HTTPBasicAuth
import json
requests.packages.urllib3.disable_warnings()



def post(ur):
    headers = {'Content-Type': 'application/json'}
    body = {"description":"Tower CLI", "application": "null" , "scope":"write"}
    r = requests.post('%s/api/v2/users/1/personal_tokens/'%ur, auth=HTTPBasicAuth('admin', 'password'),headers=body, verify=False)
    #r = requests.get('http://192.168.0.105/api/v2/job_templates', auth=HTTPBasicAuth('admin', 'password'))
    data = json.loads(r.text)
    print data["token"]
fich = open("env.json","r")
tempd = json.load(fich)
prod = tempd["prod"]
stage = tempd["stage"]
parser = argparse.ArgumentParser()
parser.add_argument("-e")
args=parser.parse_args()
if args.e == "prod":
	post(prod[0])
elif args.e == "stage":
	post(stage[0])
else:
	print "missing arguments"
