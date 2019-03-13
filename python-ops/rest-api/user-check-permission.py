#!/usr/bin/python
#execution : python user-check.py -u nik-test-1234
#execution : python user-check.py -i 13 -a 112

import requests,argparse
from requests.auth import HTTPBasicAuth
import json


headers = {'Content-Type': 'application/json'}
def check_user_i(role):
                    rr = requests.get('http://localhost/api/v2/users/?username=mike-1234', auth=HTTPBasicAuth('nik', 'nik@1234'))
                    data = json.loads(rr.text)
                    id = data["results"][0]["id"]
                    body = {"id":int(id)}
                    r2 = requests.post('http://localhost/api/v2/roles/%s/users/'%role,headers=headers,json=body,auth=HTTPBasicAuth('nik', 'nik@1234'), verify=False)
                    #print "access has been given %s to id: %s"%(r2.status_code,id)
                    print "%s access has been given to id %s"%(r2.status_code,id)


def check_user_u(username):
              r = requests.get('http://localhost/api/v2/projects/13/access_list/?search=%s'%username, auth=HTTPBasicAuth('nik', 'nik@1234'))
              data = json.loads(r.text)
              if data["count"] == 0:
                    print "user:%s does not exist ."%username
              else:
                    uid = data["results"][0]["id"]
                    print "username: %s id: %s"%(username,uid)

if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-u")
	      parser.add_argument("-a")
        args = parser.parse_args()
        if (args.u is None) and (args.a is not None):
                check_user_i(args.a)
        elif (args.u is not None) and (args.a is None):
                check_user_u(args.u)
        else:
                print("Missing arguments .")

