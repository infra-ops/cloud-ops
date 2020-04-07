#python inv.py -a host_list -u http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo

import csv,datetime
import json,socket
import requests
import re,time
import argparse
from datetime import datetime
from requests.auth import HTTPBasicAuth
import re,random
import subprocess


def org_name(addr,tok,org_id):
    headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
    r = requests.get("%s/api/v2/organizations/%s/"%(addr,org_id),headers = headers)
    data = json.loads(r.text)
    org = data["name"]
    return org
def host_list(addr,tok):
        fo = open("/home/nik/Desktop/report/%s.csv"%str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),"w+")
        nex = "/api/v2/hosts/"
        #%s%s?page=%s&page_size=100"
        all_data=[]
        while True:    
            headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
            r0 = requests.get("%s%s"%(addr,nex),headers=headers)
            data = json.loads(r0.text)
            for i in range(0,len(data["results"])):
                host_name = data["results"][i]["name"]
                created = data["results"][i]["created"]
                modified = data["results"][i]["modified"]
                inv_name = data["results"][i]["summary_fields"]["inventory"]["name"]
                org_id = data["results"][i]["summary_fields"]["inventory"]["organization_id"]
                full_name_org = org_name(addr,tok,org_id)
                gf = full_name_org.split("_")[-1]
                gb = full_name_org.replace(gf,"")
                print("%s\t%s\t%s\t%s\t%s\t%s\t%s"%(inv_name,host_name,created,modified,full_name_org,gb,gf))
                all_data.append([inv_name,host_name,created,modified,full_name_org,gb,gf])
            if str(data["next"]) == "None":
                break
            else:
                nex = str(data["next"])
        writer=csv.writer(fo)
        writer.writerow(["INVENTORY NAME","HOSTNAME","CREATED DATE","MODIFIED DATE","ORGNAME","GB","GF"])
        for row in all_data:
            writer.writerow(row)
        


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u")
    parser.add_argument("-a")
    parser.add_argument("-t")
    args = parser.parse_args()
    now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("script started at: %s"%now)
    if (args.a is not None) and (args.a in ["host_list"]):    
        if args.a == "host_list":
            host_list(args.u,args.t)
            now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            print("script ended at: %s"%now)
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

   










