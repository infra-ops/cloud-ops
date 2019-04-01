import requests,argparse
from requests.auth import HTTPBasicAuth
import json,yaml








headers = {'Content-Type': 'application/json','Authorization':'Bearer S8qGItb7fe1VwFjX8yX3aH96BXHWdK' }


def test():
              u1 = 'http://localhost/api/v2/jobs/?job_type=run&launch_type=manual&page=1&started__gt=2019-03-20T00:00&started__lt=2019-03-26T00:00&page_size=100'
              r1 = requests.get(u1,headers=headers,verify=False)
              data = json.loads(r1.text)
              print data

test()


