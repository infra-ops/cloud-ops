import datetime
import requests
import sys

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

arg = sys.argv[1]

def senc(arg):
    st = ''
    st+=arg+'\n'
    for k in range(3):
        try:
       sum= 0

    for i in range(len(string)) :
        sum = sum + ord(string[i])

    temp = sum % 256  #mod256
    rem = (temp ^ 0xFF) + 1 #two's complement, hard way (one's complement + 1)
    rem = -temp  #two's complement, easier way
    return '%2X' % (rem & 0xFF)

print calc_checksum('this is new')
print calc_checksum('00300005000')
     
            
            
            
            
        except:
            pass

    f2 = open('status'+current_time_string+'.txt', 'a')
    f2.write(st)
    f2.close()
    
def fenc(arg):
    f1 = open(arg, 'r')

    a = f1.readlines()
    encrypts = [encrypt.strip() for url in a ]
    encrypt.remove('')

    for i in encrypts:
        print i
        st = ''
        st+=i+'\n'
        for k in range(3):
            try:
                
                
sum= 0

    for i in range(len(string)) :
        sum = sum + ord(string[i])

    temp = sum % 256  #mod256
    rem = (temp ^ 0xFF) + 1 #two's complement, hard way (one's complement + 1)
    rem = -temp  #two's complement, easier way
    return '%2X' % (rem & 0xFF)

print calc_checksum('this is new')
print calc_checksum('00300005000')
                
                
                
            except:
                pass

        f2 = open('status'+current_time_string+'.txt', 'a')
        f2.write(st)
        f2.close()

    f1.close()

if 'enc' in arg:
    senc(arg)
else:
    fenc(arg)




