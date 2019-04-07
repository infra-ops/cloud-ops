import requests,argparse
from requests.auth import HTTPBasicAuth
import json
requests.packages.urllib3.disable_warnings()



#http://localhost/api/v2/users/?username=%s


def post(user,ur):
    headers = {'Content-Type': 'application/json'}
    body = {"description":"Tower CLI", "application": "null" , "scope":"write"}
    req = requests.get('%s/api/v2/users/?username=%s'%(ur,user), auth=HTTPBasicAuth('admin', 'password'),headers=body, verify=False)
    dat = json.loads(req.text)
    id = dat["results"][0]["id"]
    r = requests.post('%s/api/v2/users/%s/personal_tokens/'%(ur,id), auth=HTTPBasicAuth('admin', 'password'),headers=body, verify=False)
    #r = requests.get('http://192.168.0.105/api/v2/job_templates', auth=HTTPBasicAuth('admin', 'password'))
    data = json.loads(r.text)
    print data["token"]
fich = open("env.json","r")
tempd = json.load(fich)
prod = tempd["prod"]
stage = tempd["stage"]
parser = argparse.ArgumentParser()
parser.add_argument("-e")
parser.add_argument("-u")
args=parser.parse_args()
if (args.e == "prod") and (args.u is not None):
	post(args.u,prod[0])
elif (args.e == "stage") and (args.u is not None):
	post(args.u,stage[0])
else:
	print "missing arguments"
