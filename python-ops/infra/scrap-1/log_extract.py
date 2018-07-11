import re

f1 = open('test3', 'r')
for line in f1:
    match = re.findall( r'^([0-9]+(?:\.[0-9]+){3})', line )
    ip_address = match[0]
    
    match = re.findall( r'HTTP/1.1\" (\d*) ', line )
    status_code = match[0]
    
    print ip_address + "-" + status_code
    
f1.close()