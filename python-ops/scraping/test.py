import subprocess

'''
for ping in range(3):
    address = "127.0.0.1"
    r = subprocess.call(['ping', '-c', '3', address])
    if r==0:
        print 'ping to', address, 'ok'
    elif r==2:
        print 'no reponse'
    else:
        print 'fail'
'''

import os
arg = sys.
address = 'yahiiiii.com'

for i in range(3):
    reponse = os.system("ping -c 3 "+address)
    if reponse==0:
        print address+' ok'
    else:
        print address+' failed'
