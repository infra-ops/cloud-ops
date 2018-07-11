import time
import subprocess

cur_date=time.strftime("%d-%m-%Y")
report1="port_listen_Jio-Social_"+cur_date+".csv"
rep1=open(report1,'a')

report2="port_not_listen_Jio-Social_"+cur_date+".csv"
rep2=open(report2,'a')

def run_cmd(ip,usr,pwd,port,ser):
    cmd="sshpass -p "+pwd+" ssh -o StrictHostKeyChecking=no "+usr+"@"+ip+" netstat -plan | grep :"+port+" | grep -iE '(LISTEN|tcp|udp)'"
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #print output
    if output:
       r1=ip+","+port+","+"LISTEN\n"
       rep1.write(r1)
    else:
       r2=ip+","+port+","+"NOT LISTENING\n"
       rep2.write(r2)

#starting point - main
with open("rem.txt") as file:
     for line in file:
         ip,usr,pwd,port,ser=line.split(',')
         run_cmd(ip,usr,pwd,port,ser)
         time.sleep(2)

now=time.strftime("%c")
endline="\n========================= "+now+" =================================\n\n"
rep1.write(endline)
rep2.write(endline)

rep1.close()
rep2.close()


