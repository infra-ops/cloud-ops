#!/usr/bin/python

import csv,datetime
import json,socket
import requests
import re,time
import argparse
from datetime import datetime
from requests.auth import HTTPBasicAuth
import re
import subprocess


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
        
def add_single_user(uro,tok,org,user):
    headers = {'Content-Type': 'application/json','Authorization':'Bearer %s'%tok }
    r1 = requests.get('%s/api/v2/organizations/?search=%s'%(uro,org),headers=headers,verify=False)
    data = json.loads(r1.text)
    role_adm=data["results"][0]["summary_fields"]["object_roles"]["admin_role"]["id"]
    print("admin_role:%s"%role_adm)  
    rr = requests.get('%s/api/v2/users/?username=%s'%(uro,user),headers=headers,verify=False)
    data = json.loads(rr.text)
    idd = data["results"][0]["id"]
    body = {"id":int(idd)}
    r2 = requests.post('%s/api/v2/roles/%s/users/'%(uro,role_adm),headers=headers,json=body,verify=False)
    #print "access has been given %s to id: %s"%(r2.status_code,id)
    print("%s access has been given to id %s"%(r2.status_code,idd)) 
def add_multi_user(uro,tok,org,ff):
    fo = open(ff,"r")
    for user in fo:
        add_single_user(uro,tok,org,user.replace("\n",""))
    fo.close()
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l")
    parser.add_argument("-t")
    parser.add_argument("-o")
    parser.add_argument("-m")
    parser.add_argument("-a")
    parser.add_argument("-u")
    parser.add_argument("-q")
    args = parser.parse_args()
    now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("script started at: %s"%now)

    if (args.a is not None) and (args.a in ["permi", "suser_permi", "multi_permi", "assign_single_permi", "assign_multi_permi","single_user_add","multi_user_add"]):
        if args.a == "permi":
            object_role(args.l,args.t,args.o)
        elif args.a == "suser_permi":
            check_single_user_get(args.l,args.t,args.o,args.u)   
        elif args.a == "multi_permi":
            check_multiple_users_get(args.l,args.t,args.q,args.o)
        elif args.a == "assign_single_permi":
            check_single_user_post(args.l, args.t, args.m, args.u)
        elif args.a == "assign_multi_permi":
            #users = open(args.q, "r").readlines()    
            check_multiple_users_post(args.l, args.t, args.q, args.m)
        elif args.a == "single_user_add":
            #users = open(args.q, "r").readlines()    
            add_single_user(args.l, args.t, args.o, args.u)
        elif args.a == "multi_user_add":
            add_multi_user(args.l,args.t,args.o,args.q)
        else:
            print("Error")
            return None
        now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print("script ended at: %s"%now)
    else:
        print("kindly parse correct key")
        return None

if __name__ == "__main__":
    main()









#permi
#suser_permi
#multi_permi
#assign_single_permi
#assign_multi_permi
#assign_single_per
 #assign_multi_per

#new

#[GET]
#python user.py -a permi        -l http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -o devops-test  -u mike-1234
#python user.py -a suser_permi  -l http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -o devops-test  -q user.txt
#python user.py -a multi_permi    -l http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -o devops-test

#[POST]
#python user.py  -a assign_single_permi -l  http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -m 59 -u bob45
#python user.py  -a assign_multi_permi  -l https://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -m 59 -q user.txt
#python user.py  -a single_user_add  -l  http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo  -o devops-test -u bob45
#python user.py  -a multi_user_add   -l http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo   -o devops-test -q user.txt
