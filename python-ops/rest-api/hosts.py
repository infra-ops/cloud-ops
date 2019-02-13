import json
import requests
from requests.auth import HTTPBasciAuth
 
url = 'http://localhost/api/v2/hosts'
 
r = requests.get(url, auth=HTTPBasicAuth('admin', password))
 
data = r.json()  #sometimes r.json() trow exception, is so then change to r.text()  to extractt ip below
 
 
pr_data=json.loads(data)
""" extract host but first test above  code
ips=list()
 
for vr in range(3):
    ips.append(pr_data["results"][vr]["variables"])
 
print(ips)
 
"""
