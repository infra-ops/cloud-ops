#!/usr/bin/python
#[GET]
#python check-user.py -p devops-pune-test-api-permission 
#python check-user.py -p devops-pune-test-api-permission -u mike-1234
#python check-user.py -p devops-pune-test-api-permission -l user-list-2.yml

#[POST]
#python user-check.py -a 33 -u bob-1234
#python user-check.py -a 33 -l user-list.yml

import requests,argparse
from requests.auth import HTTPBasicAuth
import json,yaml


headers = {'Content-Type': 'application/json','Authorization':'Bearer S8qGItb7fe1VwFjX8yX3aH96BXHWdK' }


def object_role(project):
              r1 = requests.get('http://localhost/api/v2/projects/?search=%s'%project,headers=headers,verify=False)
              data = json.loads(r1.text)
              roles=data["results"][0]["summary_fields"]["object_roles"]
	      role_adm=roles["admin_role"]["id"]
              role_use=roles["use_role"]["id"]
	      role_update=roles["update_role"]["id"]
	      role_read=roles["read_role"]["id"]
	      print "admin_role:%s"%role_adm
	      print "use_role:%s"%role_use
	      print "update_role:%s"%role_update
              print "read_role:%s"%role_read
def check_single_user_get(project,username):
              r1 = requests.get('http://localhost/api/v2/projects/?search=%s'%project,headers=headers,verify=False)
              data = json.loads(r1.text)
              pr = data["results"][0]['id']
              r = requests.get('http://localhost/api/v2/projects/%s/access_list/?search=%s'%(pr,username),headers=headers,verify=False)
              data2 = json.loads(r.text)
              if data2["count"] == 0:
                    print "user:%s does not exist ."%username
              else:
                    uid = data2["results"][0]["id"]
                    print "username: %s id: %s"%(username,uid)


def check_multiple_users_get(filen,project):
              ymlfile=open(filen,"r")
              fdata=yaml.load(ymlfile)
              usernames=fdata[0]["users"]
              for username in usernames:
                  check_single_user_get(project,username)

def check_single_user_post(role,uid):
                    rr = requests.get('http://localhost/api/v2/users/?username=%s'%uid,headers=headers,verify=False)
                    data = json.loads(rr.text)
                    id = data["results"][0]["id"]
                    body = {"id":int(id)}
                    r2 = requests.post('http://localhost/api/v2/roles/%s/users/'%role,headers=headers,json=body,verify=False)
                    #print "access has been given %s to id: %s"%(r2.status_code,id)
                    print "%s access has been given to id %s"%(r2.status_code,id)


def check_multiple_users_post(filen,role):
              ymlfile=open(filen,"r")
              fdata=yaml.load(ymlfile)
              usernames=fdata[0]["users"]
              for uid in usernames:
                    rr = requests.get('http://localhost/api/v2/users/?username=%s'%uid,headers=headers,verify=False)
                    data = json.loads(rr.text)
                    id = data["results"][0]["id"]
                    body = {"id":int(id)}
                    r2 = requests.post('http://localhost/api/v2/roles/%s/users/'%role,headers=headers,json=body,verify=False)
                    #print "access has been given %s to id: %s"%(r2.status_code,id)
                    print "%s access has been given to id %s"%(r2.status_code,id)

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-p")
        parser.add_argument("-u")
	parser.add_argument("-a")
        parser.add_argument("-i")
        parser.add_argument("-l")
        args = parser.parse_args()


        
        if (args.u is None) and (args.a is None) and (args.p is not None) and (args.l is not None) and (args.i is None):
                check_multiple_users_get(args.l,args.p)
	elif (args.u is None) and (args.a is None) and (args.l is None) and (args.i is None)and (args.p is not None):
		object_role(args.p)
        elif (args.u is not None) and (args.a is not None) and (args.l is None) and (args.i is None)and (args.p is None):
                check_single_user_post(args.a,args.u)
        elif (args.u is not None) and (args.p is not None) and (args.a is None) and (args.l is None) and (args.i is None):
                check_single_user_get(args.p,args.u)
        elif (args.u is None) and (args.a is not None) and (args.l is not None) and (args.i is None)and (args.p is None):
		check_multiple_users_post(args.l,args.a)
	else:
                print("Missing arguments")
main()
