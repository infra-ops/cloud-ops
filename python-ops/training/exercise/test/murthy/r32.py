import re

name = "Murthy Raju"
house_number = "3/3"
city = "Chennai"
age = 50
weight = 72.5


"""
s = "{} lives in {}".format(name, city)
print s
"""

#s = "Murthy Raju lives in Chennai and his email Ids are murthyraju@gmail.com and murthyraju123@gmail.com"

#match = re.search(r'\w+@\w+', s)
#match = re.search(r'\w+@[\w.]+', s)
#match = re.search(r'\S+@\S+\. \S+' ,s)
#matches = re.findall(r'\S+@\S+\.\S+',s)
#print match.group()
#print matches

p = "tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      1131/nginx"
matches = re.findall("^[\w\s\d\.:]+:(%s)\s+.*$"  p)
print matches


#n = "172.31.68.145 - - [24/Apr/2018:07:41:22 +0000] "GET / HTTP/1.1" 200 396 "-" "ELB-HealthChecker/2.0""
#match = re.findall( r'[0-9]+(?:\.[0-9]+){3}', n)
#print match






















