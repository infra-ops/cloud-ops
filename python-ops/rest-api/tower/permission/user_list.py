#python inv.py -a user_list -u http://192.168.56.117 -t jge72IFPtqPvYsflypTkFQk79jgAyo

import csv,datetime
import json,socket
import requests
import re,time
import argparse
from datetime import datetime
from requests.auth import HTTPBasicAuth
import re,random
import subprocess



def user_list(addr,tok):
        headers = {'Content-Type': 'application/json','Authorization': 'Bearer %s'%tok }
        csv_data = []
        url = "%s/api/v2/users/"%(addr)
        while True:
            r0 = requests.get(url,headers=headers)
            data0 = json.loads(r0.text)
            cc = int(data0["count"])
            print(cc)
            rez = data0["results"]
            for user in rez:
                csv_data.append([user["username"],user["email"]])
            if str(data0["next"]) == "None":
                break
            else:
                url = "%s%s"%(addr,str(data0["next"]))
                continue
        now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        with open("%s.csv"%now,"w+") as o:
            writer=csv.writer(o)
            writer.writerow(["username","email"])
            for dd in csv_data:
                writer.writerow(dd)
#let me see this in postman



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u")
    parser.add_argument("-a")
    parser.add_argument("-t")
    args = parser.parse_args()
    now = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("script started at: %s"%now)
    if (args.a is not None) and (args.a in ["user_list"]):    
        if args.a == "user_list":
            user_list(args.u,args.t)
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

   










