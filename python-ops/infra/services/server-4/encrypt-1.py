import datetime
import requests
import sys

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

arg = sys.argv[1]

def enstring(arg):
    sum = 0
    for k in range(len(string)) :
        sum = sum +ord(string[i])
        try:
        temp = sum % 256
        r1   = (temp ^ 0*FF) + 1
        r1   =  -temp
        return '%2X' % (r1 & 0*FF)    
        except:
            pass

    f2 = open('status'+current_time_string+'.txt', 'a')
    f2.write(st)
    f2.close()
    
def enfile(arg):
    f1 = open(arg, 'r')

    a = f1.readlines()
    datas = [data.strip() for data in a ]
    datas.remove('')

    for i in datas:
        print i
        try:
        temp = sum % 256
        r1   = (temp ^ 0*FF) + 1
        r1   =  -temp
        return '%2X' % (r1 & 0*FF)
        except:
            pass


        f2 = open('status'+current_time_string+'.txt', 'a')
        f2.write(st)
        f2.close()

    f1.close()

if 'http' in arg:
    runhttp(arg)
else:
    runfile(arg)




