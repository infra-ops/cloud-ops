import subprocess
import argparse
import pandas as pd
import re
import  json
from  bson.json_util  import  dumps
import plotly as py

def cmds(ip,usr,pwd):
        #this function will initialize all the commands and give them to run function for execution and return the output as well
        ip=str(ip)
        ip2 = "sshpass -p "+pwd+" ssh "+usr+"@"+ip+" "+"sudo yum check-update"
        p = subprocess.Popen(ip2 ,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
        out, err=p.communicate()
        return out
def json_read_file(json_file):
#this function will get all hosts ,usernames and passwords and pass them for execution , after the execution it'll print the output and write to csv file
        f = open(json_file,"r+")
        datax = json.load(f)
        keyz = datax.keys()
        status_machine=[]
        for i in range(0,len(keyz)):
                try:
                                hosts = datax[keyz[i]]["hosts"]
                                user = datax[keyz[i]]["vars"]["ansible_ssh_user"]
                                psw = datax[keyz[i]]["vars"]["ansible_ssh_pass"]
				filex = open("server%s.html"%str(i+1),"w+")
				for ip in hosts:
					new=[]
					final=[]
                                        data=cmds(ip,user,psw)
					data=data.split("\n")
					del data[:2]
					filex.write("<html><table border='1'><tr><th>Package Name</th><th>Versions</th><th>Repo</th></tr>")
					for i in data:
						i=i.split(" ")
						new.append(i)
					for lo in new:
							lo=filter(None, lo)
							final.append(lo)
					del final[len(final)-1]
					for fl in range(0,len(final)-1):
						try:
							if len(final[fl]) != 3:
								final[fl]=final[fl]+final[fl+1]
								del final[fl+1]
						except:
							break
					for fl in range(0,len(final)-1):
							filex.write("<tr>\n")
							for it in final[fl]:
								filex.write("<td>%s</td>\n"%it)
							filex.write("</tr>")
                                        continue
                except Exception as e:
				print e
                                continue

if __name__ == '__main__':
#here will be arguments control and initialisation
        parser = argparse.ArgumentParser()
        parser.add_argument("-i")
        args = parser.parse_args()
        if args.i is not None:
                json_read_file(args.i)
        else:
                print "Missing arguments ."

