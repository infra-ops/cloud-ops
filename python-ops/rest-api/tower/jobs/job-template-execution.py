import requests
from requests.auth import HTTPBasicAuth
import json
requests.packages.urllib3.disable_warnings()



def post():
    #params = {'token': 'UxSFmLFPNOG6vEHvEwpX0PxbkUO80s'}
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://192.168.0.105/api/v2/job_templates/10/launch/', auth=HTTPBasicAuth('admin', 'password'),  headers=headers, verify=False)
    #r = requests.get('http://192.168.0.105/api/v2/job_templates', auth=HTTPBasicAuth('admin', 'password'))
    print r.text

post()
