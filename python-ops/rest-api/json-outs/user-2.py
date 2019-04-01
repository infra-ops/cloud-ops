#!/usr/bin/python
#[GET]
#python check-user.py -p devops-pune-test-api-permission -u mike-1234
#python check-user.py -p devops-pune-test-api-permission -l user-list-2.yml

#[POST]
#python user-check.py -a 33 -u bob-1234
#python user-check.py -a 33 -l user-list.yml

import requests,argparse
from requests.auth import HTTPBasicAuth
import json,yaml

fich = open("env.json","r")
#headers = {'Content-Type': 'application/json','Authorization':'Bearer S8qGItb7fe1VwFjX8yX3aH96BXHWdK' }
tempd = json.load(fich)
prod = tempd["prod"]
stage = tempd["stage"]
def object_role(uro,tok,project):
	      headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%tok }
              r1 = requests.get('%s/api/v2/projects/?search=%s'%(uro,project),headers=headers,verify=False)
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
def check_single_user_get(uro,tok,project,username):
	      headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%tok }
              r1 = requests.get('%s/api/v2/projects/?search=%s'%(uro,project),headers=headers,verify=False)
              data = json.loads(r1.text)
              pr = data["results"][0]['id']
              r = requests.get('%s/api/v2/projects/%s/access_list/?search=%s'%(uro,pr,username),headers=headers,verify=False)
              data2 = json.loads(r.text)
              if data2["count"] == 0:
                    print "user:%s does not exist ."%username
              else:
                    uid = data2["results"][0]["id"]
                    print "username: %s id: %s"%(username,uid)


def check_multiple_users_get(uro,tok,filen,project):
              ymlfile=open(filen,"r")
              fdata=yaml.load(ymlfile)
              usernames=fdata[0]["users"]
              for username in usernames:
                  check_single_user_get(project,username)

def check_single_user_post(uro,tok,role,uid):
		    headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%tok }
                    rr = requests.get('%s/api/v2/users/?username=%s'%(uro,uid),headers=headers,verify=False)
                    data = json.loads(rr.text)
                    id = data["results"][0]["id"]
                    body = {"id":int(id)}
                    r2 = requests.post('%s/api/v2/roles/%s/users/'%(uro,role),headers=headers,json=body,verify=False)
                    #print "access has been given %s to id: %s"%(r2.status_code,id)
                    print "%s access has been given to id %s"%(r2.status_code,id)


def check_multiple_users_post(uro,tok,filen,role):
              ymlfile=open(filen,"r")
              fdata=yaml.load(ymlfile)
              usernames=fdata[0]["users"]
	      headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%tok }
              for uid in usernames:
                    rr = requests.get('%s/api/v2/users/?username=%s'%(uro,uid),headers=headers,verify=False)
                    data = json.loads(rr.text)
                    id = data["results"][0]["id"]
                    body = {"id":int(id)}
                    r2 = requests.post('%s/api/v2/roles/%s/users/'%(uro,role),headers=headers,json=body,verify=False)
                    #print "access has been given %s to id: %s"%(r2.status_code,id)
                    print "%s access has been given to id %s"%(r2.status_code,id)

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-p")
        parser.add_argument("-u")
	parser.add_argument("-a")
        parser.add_argument("-i")
        parser.add_argument("-l")
	parser.add_argument("-e")
        args = parser.parse_args()
	if args.e == "prod":
		ur = prod[0]
		toke = prod[1]
        	if (args.u is None) and (args.a is None) and (args.p is not None) and (args.l is not None) and (args.i is None):
        	        check_multiple_users_get(ur,toke,args.l,args.p)
		elif (args.u is None) and (args.a is None) and (args.l is None) and (args.i is None)and (args.p is not None):
			object_role(ur,toke,args.p)
        	elif (args.u is not None) and (args.a is not None) and (args.l is None) and (args.i is None)and (args.p is None):
        	        check_single_user_post(ur,toke,args.a,args.u)
        	elif (args.u is not None) and (args.p is not None) and (args.a is None) and (args.l is None) and (args.i is None):
        	        check_single_user_get(ur,toke,args.p,args.u)
        	elif (args.u is None) and (args.a is not None) and (args.l is not None) and (args.i is None)and (args.p is None):
			check_multiple_users_post(ur,toke,args.l,args.a)
		else:
        	        print("Missing arguments")
        elif args.e == "stage":
                ur = stage[0]
                toke = stage[1]
                if (args.u is None) and (args.a is None) and (args.p is not None) and (args.l is not None) and (args.i is None):
                        check_multiple_users_get(ur,toke,args.l,args.p)
                elif (args.u is None) and (args.a is None) and (args.l is None) and (args.i is None)and (args.p is not None):
                        object_role(ur,toke,args.p)
                elif (args.u is not None) and (args.a is not None) and (args.l is None) and (args.i is None)and (args.p is None):
                        check_single_user_post(ur,toke,args.a,args.u)
                elif (args.u is not None) and (args.p is not None) and (args.a is None) and (args.l is None) and (args.i is None):
                        check_single_user_get(ur,toke,args.p,args.u)
                elif (args.u is None) and (args.a is not None) and (args.l is not None) and (args.i is None)and (args.p is None):
                        check_multiple_users_post(ur,toke,args.l,args.a)
                else:
                        print("Missing arguments")
	else:
		print "Missing argument -e"
main()
