#python inv.py -u 192.168.10.117 -t  -i -f ip.txt

import csv,datetime
import json,socket
import requests
import re,time
import argparse
from datetime import datetime
from requests.auth import HTTPBasicAuth
import re,random
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
        
def group_host_add(addr, tok, group, idd, iplist):
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
        r0 = requests.get("%s/api/v2/groups/%s/hosts/" % (addr, group),headers=headers)
        data0 = json.loads(r0.text)
        cc = int(data0["count"])
        print("before addition count= %s"%cc)
        all_ids=[]
        for ip in iplist:
            body = {"name":"%s" % str(ip).replace("\n",""), "enabled": "true", "inventory": idd}
            url = '%s/api/v2/groups/%s/hosts/' % (addr, group)
            r = requests.post(url, headers=headers, json=body)
            host_name= ip.replace("\n","")
            r1 = requests.get("%s/api/v2/hosts/?name=%s" % (addr, host_name), headers=headers)
            data = json.loads(r1.text)
            try:    
                host_id = data["results"][0]["id"]
                all_ids.append(host_id)
            except:
                all_ids.append("%s ip quota exceeded"%host_name)
        with open("ids_added.txt","w+") as o:
            #print("ids")
            for i in all_ids:
                #print(i)
                o.write("%s\n"%str(i))
        r0 = requests.get("%s/api/v2/groups/%s/hosts/"%(addr, group),headers=headers)
        data0 = json.loads(r0.text)
        cc = int(data0["count"])
        print("after addition count= %s"%cc)  
        
           
def host_spec_del(addr,tok,idd,num):
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
    rx = requests.get("%s/api/v2/inventories/%s/hosts/"%(addr,idd),headers=headers)
    #we will get ids of hosts from above ep ,among all ips we need to parse 50 ids to delete command
    datax = json.loads(rx.text)
    cc = int(datax["count"])
    print("before deletion count= %s"%cc)
    j=0
    urls="%s/api/v2/inventories/%s/hosts/?page=1"%(addr,idd)
    while True:
        try:
            if j == int(num):
                break
            else:
                headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
                rx = requests.get(urls,headers=headers)
                #we will get ids of hosts from above ep ,among all ips we need to parse 50 ids to delete command
                datax = json.loads(rx.text)
                hosts_ids = []
                sizer = datax["results"]
                for q in range(len(sizer)):
                    idx = datax["results"][q]["id"]
                    hosts_ids.append(idx)
                ee = 0
                while True:
                    try:
                        if j == int(num):
                            break
                        else:
                            r2 = requests.delete("%s/api/v2/hosts/%s/"%(addr,hosts_ids[ee]), headers=headers)
                            ee = ee+1
                            j=j+1
                    except IndexError:
                        break
                time.sleep(1)
        except Exception as e:
            print(e)
            break
    rx = requests.get("%s/api/v2/inventories/%s/hosts/"%(addr,idd),headers=headers)
    #we will get ids of hosts from above ep ,among all ips we need to parse 50 ids to delete command
    datax = json.loads(rx.text)
    cc = int(datax["count"])
    print("after deletion count= %s"%cc)   



#create inv

def create_inv(addr,tok,org,name):
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
    body = {"organization": int(org), "kind": "","name": name}
    url = '%s/api/v2/inventories/'%addr
    r = requests.post(url, headers=headers, json=body)
    datax = json.loads(r.text)
    cc = int(datax["id"])#prob is in this line no, look
    print("id of inv %s: %s"%(name,cc))
    



#delete 
def delete_inv(addr,tok,idd):
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
    url = '%s/api/v2/inventories/%s/'%(addr, idd)
    r = requests.delete(url, headers=headers)
    print("following %s got deleted"%idd)

def inv_add_v2(addr,tok,idd,group,num):
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
        rx = requests.get("%s/api/v2/groups/%s/hosts/"%(addr,group),headers=headers)#first count
        #we will get ids of hosts from above ep ,among all ips we need to parse 50 ids to delete command
        datax = json.loads(rx.text)
        cc = int(datax["count"])
        print("before addition count= %s"%cc)
        url="%s/api/v2/hosts/"%addr
        all_ips = []
        while True:        
                try:
                    r0 = requests.get(url,headers=headers)
                    data0 = json.loads(r0.text)
                    nx = data0["next"]
                    results = data0["results"]
                    for ix in results:
                            all_ips.append(ix["name"])
                    url = "%s%s"%(addr,nx)
                except Exception as e:
                    break
        q = 0
        ff =  set(all_ips)
        for ip in ff:
            if q == int(num):
                break
            else:    
                body = {"name":ip,"description":"Hello World"}
                url = '%s/api/v2/groups/%s/hosts/' % (addr, group)#add to group
                r = requests.post(url, headers=headers, json=body)
                q=q+1
        rx = requests.get("%s/api/v2/groups/%s/hosts/"%(addr,group),headers=headers)#count after add
        #we will get ids of hosts from above ep ,among all ips we need to parse 50 ids to delete command
        datax = json.loads(rx.text)
        cc = int(datax["count"])
        print("after addition count= %s"%cc)

            #print("before addition count= %s"%cc)
            
        #print("after addition count= %s"%cc)


#############
#### NEW ####
#############
#python inv.py -a  add -u http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 3  -f ip_add.txt
#python inv.py -a  del_all -u http://192.168.10.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 3
#python inv.py -a  del_spec -u http://192.168.10.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 3 -f ip_del.txt
#python inv.py -a  group_add_host -u http://192.168.10.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -g 2 -i 3 -f ip_add.txt
#python inv.py -a  host_spec_del -u http://192.168.10.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 4  -d 10
#python inv.py -a  create_inv -u http://192.168.10.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo -o 2 -n test7
#python inv.py -a  del_inv -u http://192.168.56.117   -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 3
#python inv.py -a  add_spec    -u http://192.168.56.117   -t jge72IFPtqPvYsflypTkFQk79jgAyo -i 14 -g 12 -s 10


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u")
    parser.add_argument("-a")
    parser.add_argument("-o")
    parser.add_argument("-n")
    parser.add_argument("-t")
    parser.add_argument("-i")
    parser.add_argument("-f") #File
    parser.add_argument("-g") #Group ID
    parser.add_argument("-d")
    parser.add_argument("-s")

    args = parser.parse_args()
    now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("script started at: %s"%now)

    #if (args.a is not None) and (args.a in ["add", "del_all", "del_spec", "group_add_host", "host_spec_del","create_inv","del_inv"]):
    if (args.a is not None) and (args.a in ["add", "del_all", "del_spec", "group_add_host", "host_spec_del","create_inv","del_inv","add_spec"]):    
        if args.a == "add":
            ips = open(args.f,"r").readlines()
            inv_add(args.u, args.t, args.i, ips)
        elif args.a == "del_all":
            inv_del(args.u, args.t, args.i)
        elif args.a == "del_spec":
            inv_spec_del(args.u, args.t, args.i, args.f)
        elif args.a == "group_add_host":
            ips = open(args.f,"r").readlines()
            group_host_add(args.u, args.t, args.g, args.i, ips)
        elif args.a == "host_spec_del":
           host_spec_del(args.u, args.t, args.i, args.d)
        elif args.a == "create_inv":
            create_inv(args.u,args.t,args.o,args.n)
        elif args.a == "del_inv":       
            delete_inv(args.u,args.t,args.i)
        elif args.a == "add_spec":       
            inv_add_v2(args.u,args.t,args.i,args.g,args.s)    
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
