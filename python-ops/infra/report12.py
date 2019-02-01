import subprocess
import argparse
import csv
import pandas as pd
import os
import re


def gencsv():
	
	
	#-------------------clear sample.csv to empy file
        sample=open("sampleReport.csv", "w")
        sample.write("")
        sample.close()

	status_machine=[]
	
	data=cmds()
	with open("sampleReport.csv", "a") as fl:
		dataS=csv.writer(fl, delimiter=",")
		dataS.writerow(["IP","HOSTNAME","OS VERSION","CPU USAGE","MEMORY USAGE","ANSIBLE VERSION","NGINX STATUS","DB STATUS"])
		dataS.writerow([str(next(data)).replace("\n",""), str(next(data)).replace("\n",""),str(next(data)).replace("\n",""),str(next(data)).replace("\n",""), str(next(data)).replace("\n",""),str(next(data)).replace("\n",""),str(next(data)).replace("\n",""), str(next(data)).replace("\n","")])
	

	#showing data 
        rData=pd.read_csv("sampleReport.csv", index_col="IP")
        rData=rData.fillna("NO")
	rData["DB STATUS"].replace("\.0", "", regex=True, inplace=True)
	print("Report generarted, pls check  sampleReport.csv in your current Dir\n")
	print(rData)
        

def cmds():
        #ip
        ip = "hostname -I | awk '{print $1;}'"
        p1=subprocess.Popen((ip), stdout=subprocess.PIPE, shell=True)
        out,err= p1.communicate()
        yield out
        ##host
        host = "hostname -f"
        p2=subprocess.Popen((host), stdout=subprocess.PIPE, shell=True)
        out,err= p2.communicate()
        yield out
        ### os
        dist = "cat /etc/lsb-release | sed -n '2p' | cut -d \"=\" -f2"
        p3=subprocess.Popen((dist), stdout=subprocess.PIPE, shell=True)
        out,err= p3.communicate()
        yield out
        ####cpu
        cpu = "top -bn1 | grep \"Cpu(s)\" | sed \"s/.*, *\([0-9.]*\)%* id.*/\1/\" | awk '{print 100 - $1\"%\"}'"
        p4=subprocess.Popen((cpu), stdout=subprocess.PIPE, shell=True)
        out,err= p4.communicate()
        yield out
        ###mem 
        mem = "free -m | sed -n '2p' | awk '{print $3;}'"
        p5=subprocess.Popen((mem), stdout=subprocess.PIPE, shell=True)
        out,err= p5.communicate()
        yield out
        ###ans version
        ans = "ansible --version | sed -n '1p'"
        p6=subprocess.Popen((ans), stdout=subprocess.PIPE, shell=True)
        out,err= p6.communicate()
        yield out
        ###nginx
        nginx = "netstat -ntlp | grep 80 | sed -n '1p' | awk '{print $4;}' | cut -d \":\" -f2"
        p7=subprocess.Popen((nginx), stdout=subprocess.PIPE, shell=True)
        out,err= p7.communicate()
        yield out
        
         ###pg 
        pg = "netstat -ntlp | grep 5432 | awk '{print $4;}' | cut -d \":\" -f2"
        p8=subprocess.Popen((pg), stdout=subprocess.PIPE, shell=True)
        out,err= p8.communicate()
        yield out

try:
    import yaml
except ImportError as ie:
    LIB_MAP = {'yaml': 'PyYAML'}
    m = ie.message
    missing_mod = m[m.rfind(" "):].strip()
    msg = "missing python module '%s' (please install manually)\n" % missing_mod\
        + "  use: pip install %s" % LIB_MAP.get(missing_mod, missing_mod)
    error(msg)



    
def remote(ip,usr,pwd,port,ser):
    cmd="sshpass -p "+pwd+" ssh -o StrictHostKeyChecking=no "+usr+"@"+ip+" cmds "
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #print output
    #if output:
    #   r1=ip+","+port+","+"LISTEN\n"
    #   rep1.write(r1)
    #else:
    #   r2=ip+","+port+","+"NOT LISTENING\n"
    #   rep2.write(r2)










    






if __name__ == '__main__':
        gencsv()
