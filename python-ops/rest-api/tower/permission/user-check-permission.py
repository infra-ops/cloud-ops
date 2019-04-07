##!/usr/bin/python
#execution : python user-check.py -u nik-test-1234
#execution : python user-check.py -i 13 -a 112

import requests,argparse
from requests.auth import HTTPBasicAuth
import json,yaml


headers = {'Content-Type': 'application/json'}
def check_user_i(role,uid):
                    rr = requests.get('http://localhost/api/v2/users/?username=%s'%uid, auth=HTTPBasicAuth('nik', 'nik@1234'))
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
def post_user_file(filen,role):
              ymlfile=open(filen,"r")
              fdata=yaml.load(ymlfile)
              usernames=fdata[0]["users"]
              for uid in usernames:
                    rr = requests.get('http://localhost/api/v2/users/?username=%s'%uid, auth=HTTPBasicAuth('nik', 'nik@1234'))
                    data = json.loads(rr.text)
                    id = data["results"][0]["id"]
                    body = {"id":int(id)}
                    r2 = requests.post('http://localhost/api/v2/roles/%s/users/'%role,headers=headers,json=body,auth=HTTPBasicAuth('nik', 'nik@1234'), verify=False)
                    #print "access has been given %s to id: %s"%(r2.status_code,id)
                    print "%s access has been given to id %s"%(r2.status_code,id)

def check_user_file(filen):
              ymlfile=open(filen,"r")
              fdata=yaml.load(ymlfile)
              usernames=fdata[0]["users"]
              for username in usernames:
                  r = requests.get('http://localhost/api/v2/projects/13/access_list/?search=%s'%username, auth=HTTPBasicAuth('nik', 'nik@1234'))
                  data = json.loads(r.text)
                  if data["count"] == 0:
                    print "user:%s does not exist ."%username
                  else:
                    uid = data["results"][0]["id"]
                    print "username: %s id: %s"%(username,uid)
#if __name__ == '__main__':
def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-u")
	parser.add_argument("-a")
        parser.add_argument("-i")
        parser.add_argument("-l")
        args = parser.parse_args()
        if (args.u is not None) and (args.a is not None) and (args.l is None) and (args.i is None):
                check_user_i(args.a,args.u)
        elif (args.u is not None) and (args.a is None) and (args.l is None) and (args.i is None):
                check_user_u(args.u)
        elif (args.u is None) and (args.a is None) and (args.l is not None) and (args.i is None):
		check_user_file(args.l)
	elif (args.u is None) and (args.a is not None) and (args.l is not None) and (args.i is None):
		post_user_file(args.l,args.a)
	else:
                print("Missing arguments .")
main()


