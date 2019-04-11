import requests
from requests.auth import HTTPBasicAuth
import json
#requests.packages.urllib3.disable_warnings()



def post():
    headers = {'Content-Type': 'application/json'}
    r = requests.post('http://localhost/api/v2/job_templates/18/launch/', auth=HTTPBasicAuth('admin', 'password'),  headers=headers, verify=False)
    print r.text

post()
