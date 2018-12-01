import datetime
import requests
import sys
import os

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

arg = sys.argv[1]

def sping(arg):
    st = ''
    for i in range(1):
        reponse = os.system("ping -c 1 "+arg)
        if reponse==0:
            st+=arg+' ok\n'
        else:
            st+=arg+' failed\n'
        f2 = open('status'+current_time_string+'.txt', 'a')
        f2.write(st)
        f2.close()


def fping(arg):
    f1 = open(arg, 'r')
    a = f1.readlines()
    ips = [ip.strip() for ip in a ]
    st = ''
    for i in ips:
        print i
        #st+=i+'\n'
        for k in range(1):
            reponse = os.system("ping -c 1 "+i)
            if reponse==0:
                st+=i+' ok\n'
            else:
                st+=i+' failed\n'
    f2 = open('status'+current_time_string+'.txt', 'a')
    f2.write(st)
    f2.close()

if __name__=='__main__':
    if '.' in arg:
        sping(arg)
    else:
        fping(arg)



#python service.py m1.txt username ip






        









