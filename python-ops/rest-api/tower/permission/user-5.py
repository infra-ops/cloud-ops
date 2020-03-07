#!/usr/bin/python
#[GET]
#python user.py -l https://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -o devops-test  -u mike-1234
#python user.py -l https://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -o devops-test  -q user.txt

#[POST]
#python user.py -l  https://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo   -a 33 -u bob-1234
#python user.py  -l https://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo   -a 33 -q user-2.txt




import requests,argparse
from requests.auth import HTTPBasicAuth
import json,yaml



def object_role(uro,tok,org):
              headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%tok }
              r1 = requests.get('%s/api/v2/organizations/?search=%s'%(uro,org),headers=headers,verify=False)
              data = json.loads(r1.text)
              role_adm=data["results"][0]["summary_fields"]["object_roles"]["admin_role"]["id"]
              print("admin_role:%s"%role_adm)
	     
def check_single_user_get(uro,tok,org,username):
              headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%tok }
              r1 = requests.get('%s/api/v2/organizations/?search=%s'%(uro,org),headers=headers,verify=False)
              data = json.loads(r1.text)
              pr = data["results"][0]['id']
              r = requests.get('%s/api/v2/organizations/%s/access_list/?search=%s'%(uro,pr,username),headers=headers,verify=False)
              data2 = json.loads(r.text)
              if data2["count"] == 0:
                    print("user:%s does not exist ."%username)
              else:
                    uid = data2["results"][0]["id"]
                    print("username: %s id: %s"%(username,uid))


def check_multiple_users_get(uro,tok,filen,org):              
              tmp = open(filen,"r")
              for username in tmp:
                  check_single_user_get(uro,tok,org,username.replace("\n",""))
              tmp.close()
def check_single_user_post(uro,tok,role,uid):
                    headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%tok }
                    rr = requests.get('%s/api/v2/users/?username=%s'%(uro,uid),headers=headers,verify=False)
                    data = json.loads(rr.text)
                    idd = data["results"][0]["id"]
                    body = {"id":int(idd)}
                    r2 = requests.post('%s/api/v2/roles/%s/users/'%(uro,role),headers=headers,json=body,verify=False)
                    #print "access has been given %s to id: %s"%(r2.status_code,id)
                    print("%s access has been given to id %s"%(r2.status_code,idd))

def check_multiple_users_post(uro,tok,filen,role):
              usernames=open(filen,"r")
              headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%tok }
              for uid in usernames:
                    uid=uid.replace("\n","")
                    rr = requests.get('%s/api/v2/users/?username=%s'%(uro,uid),headers=headers,verify=False)
                    data = json.loads(rr.text)
                    idd = data["results"][0]["id"]
                    body = {"id":int(idd)}
                    r2 = requests.post('%s/api/v2/roles/%s/users/'%(uro,role),headers=headers,json=body,verify=False)
                    #print "access has been given %s to id: %s"%(r2.status_code,id)
                    print("%s access has been given to id %s"%(r2.status_code,idd))

def main():
        parser = argparse.ArgumentParser()
        parser.add_argument("-l")
        parser.add_argument("-t")
        parser.add_argument("-o")
        parser.add_argument("-a")
        parser.add_argument("-u")
        parser.add_argument("-q")
        args = parser.parse_args()
        if (args.o != None) and (args.a is None):
                if args.u != None:
                        object_role(args.l,args.t,args.o)
                elif args.q != None:
                        check_multiple_users_get(args.l,args.t,args.q,args.o)
                else:
                        check_single_user_get(args.l,args.t,args.o,args.u)
        elif (args.a != None) and (args.o is None):
                if args.q != None:
                        check_multiple_users_post(args.l,args.t,args.q,args.a)
                else:
                        check_single_user_post(args.l,args.t,args.a,args.u)
main()


#[GET]
#python user.py -l http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -o devops-test  -u mike-1234
#python user.py -l http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -o devops-test  -q user.txt
#python user.py -l http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -o devops-test
#[POST]
#python user.py -l  http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -a 59 -u bob45
#python user.py  -l https://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -a 59 -q user.txt




