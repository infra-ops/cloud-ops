import requests
import datetime
import smtplib
import subprocess
import time
import re



EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'xxxxxx@gmail.com'
EMAIL_HOST_PASSWORD = 'xxxxx'
EMAIL_PORT = 587

def send_mail(from_address, to_address, subject, body):

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (from_address, to_address, subject)
    msg += body

    server.sendmail(from_address, to_address, msg)
    server.quit()

    print "Done sending mail to " + to_address
    return True




current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

f_live = open("live_status_ok_" + current_time_string  + ".txt" , "w")
f_dead = open("dead_status_err_" + current_time_string  + ".txt", "w")



def run_cmd(ip,port,usr,pwd,ser):
    ser=ser.strip() #strip newline in rem.txt file since this is the last parameter
    cmd = "sshpass -p "+pwd+" ssh -q -o ConnectTimeout=5 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "+usr+"@"+ip+" ps aux |grep -i "+ser+" |grep -v grep 2>/dev/null"
    print cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    #print output
    if output:
        r1 = ip + "," + ser + "," + "RUNNING\n"
        f_live.write(r1)
    else:
        r2 = ip + "," + ser + "," + "NOT RUNNING\n"
        #f_dead.write(r2)


        FROM = "xxxxxx@gmail.com"
        TO  = "xxxxx@gmail.com"
        SUBJECT = "Service is Dead. URGENT - " + r2
        body = "Hi\nService %s is dead. do something about it urgently.\n\nMonitoring Team" % (r2)

        send_mail(FROM, TO, SUBJECT, body)

        f_dead.write(r2)

#starting point - main

f1 = open("pod")

for line in f1:
    ip, port, usr, pwd, ser = line.split(':')
    run_cmd(ip, port, usr, pwd, ser)
    time.sleep(1)



    now=time.strftime("%c")

    endline="\n========================= "+now+" =================================\n\n"

f_live.write(endline)
f_dead.write(endline)


#f_live.write()
#f_dead.close()









