#!/usr/bin/python
import time
import subprocess

cur_date=time.strftime("%d-%m-%Y")
report1="service_ok_Jio-Social_"+cur_date+".csv"
rep1=open(report1,'a')

report2="service_err_Jio-Social_"+cur_date+".csv"
rep2=open(report2,'a')

def run_cmd(ip,port,usr,pwd,ser):
    ser=ser.strip() #strip newline in rem.txt file since this is the last parameter
    cmd = "sshpass -p "+pwd+" ssh -q -o ConnectTimeout=5 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "+usr+"@"+ip+" ps aux |grep -i "+ser+" |grep -v grep 2>/dev/null"
    print cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #print output
    if output:
        r1 = ip + "," + ser + "," + "RUNNING\n"
        rep1.write(r1)
    else:
        r2 = ip + "," + ser + "," + "NOT RUNNING\n"
        rep2.write(r2)

#starting point - main
with open("pod") as file:
    for line in file:
        ip, port, usr, pwd, ser = line.split(':')
        run_cmd(ip, port, usr, pwd, ser)
        time.sleep(1)

now=time.strftime("%c")
endline="\n========================= "+now+" =================================\n\n"
rep1.write(endline)
rep2.write(endline)

rep1.close()
rep2.close()