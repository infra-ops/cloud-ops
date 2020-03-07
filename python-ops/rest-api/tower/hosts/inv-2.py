#python inv.py -u 192.168.10.117 -t  -i -f ip.txt

import csv,datetime
import json,socket
import requests
import re
import argparse
from datetime import datetime
from requests.auth import HTTPBasicAuth
import re
import subprocess


def inv_add(addr,tok,idd,iplist):
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
        r0 = requests.get("%s/api/v2/inventories/%s/hosts/"%(addr,idd),headers=headers)
        data0 = json.loads(r0.text)
        cc = int(data0["count"])
        print("before addition count= %s"%cc)
        all_ids=[]
        for ip in iplist:
            body = {"name":"%s"%str(ip).replace("\n",""),"description":"Hello World"}
            url = '%s/api/v2/inventories/%s/hosts/'%(addr,idd)
            r = requests.post(url, headers=headers, json=body)
            host_name= ip.replace("\n","")
            r1 = requests.get("%s/api/v2/hosts/?name=%s"%(addr,host_name), headers=headers)
            data = json.loads(r1.text)
            try:    
                host_id = data["results"][0]["id"]
                all_ids.append(host_id)
            except:
                all_ids.append("%s ip quota exceeded"%host_name)
        with open("ids_added.txt","w+") as o:
            print("ids")
            for i in all_ids:
                print(i)
                o.write("%s\n"%str(i))
        r0 = requests.get("%s/api/v2/inventories/%s/hosts/"%(addr,idd),headers=headers)
        data0 = json.loads(r0.text)
        cc = int(data0["count"])
        print("after addition count= %s"%cc)
        
def inv_del(addr,tok,idd):
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
        r0 = requests.get("%s/api/v2/inventories/%s/hosts/"%(addr,idd),headers=headers)
        data0 = json.loads(r0.text)
        cc = int(data0["count"])
        print("before deletion count= %s"%cc)
        hosts = data0["results"]
        all_ids = []
        for host in hosts:
            host_name=host["name"]
            r1 = requests.get("%s/api/v2/hosts/?name=%s"%(addr,host_name), headers=headers)
            data = json.loads(r1.text)
            host_id = data["results"][0]["id"]
            all_ids.append(host_id)
        print("deleted")
        for host_id in all_ids:
            r2 = requests.delete("%s/api/v2/hosts/%s/"%(addr,host_id), headers=headers)
            print("id %s deleted" % host_id)
        rx = requests.get("%s/api/v2/inventories/%s/hosts/"%(addr,idd),headers=headers)
        datax = json.loads(rx.text)
        cc = int(datax["count"])
        print("after deletion count= %s"%cc)

def inv_spec_del(addr,tok,idd,ids_file):
        temp = open(ids_file,"r")
        all_ids = temp.readlines()
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
        rx = requests.get("%s/api/v2/inventories/%s/hosts/"%(addr,idd),headers=headers)
        datax = json.loads(rx.text)
        cc = int(datax["count"])
        print("before deletion count= %s"%cc)
        print("deleted")
        for host_id in all_ids:
            r2 = requests.delete("%s/api/v2/hosts/%s/"%(addr,host_id.replace("\n","")), headers=headers)
            print("id %s deleted"%host_id.replace("\n",""))
        rx = requests.get("%s/api/v2/inventories/%s/hosts/"%(addr,idd),headers=headers)
        datax = json.loads(rx.text)
        cc = int(datax["count"])
        print("after deletion count= %s"%cc)

#############
#### OLD ####
#############
#python inv.py -a add -u http://192.168.10.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 3  -f ip_add.txt
#python inv.py -d del -u http://192.168.10.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 3
#python inv.py -d del -u http://192.168.10.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 3 -f ip_del.txt
#args = parser.parse_args()
#now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#print("script started at: %s"%now)
#if args.a != None :
#    ips = open(args.f,"r").readlines()
#    inv_add(args.u,args.t,args.i,ips)
#if (args.d != None) and (args.f == None):
#    inv_del(args.u,args.t,args.i)
#if (args.d != None) and (args.f != None):
#    inv_spec_del(args.u,args.t,args.i,args.f)
#now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
#print("script ended at: %s"%now)


#############
#### NEW ####
#############
#python inv.py -a add -u http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 3  -f ip_add.txt
#python inv.py -a del_all -u http://192.168.10.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 3
#python inv.py -a del_spec -u http://192.168.10.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 3 -f ip_del.txt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u")
    parser.add_argument("-a")
    parser.add_argument("-t")
    parser.add_argument("-i")
    parser.add_argument("-f")

    args = parser.parse_args()
    now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("script started at: %s"%now)

    if args.a is not None and args.a in ["add", "del_all", "del_spec"]:
        if args.a == "add":
            ips = open(args.f,"r").readlines()
            inv_add(args.u,args.t,args.i,ips)
        elif args.a == "del_all":
            inv_del(args.u,args.t,args.i)
        elif args.a == "del_spec":
            inv_spec_del(args.u,args.t,args.i,args.f)
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
