#!/usr/bin/python

import json


"""
x = '{"name":"smith", "designation":"cloud", "city":"oslo"}'
y = json.loads(x)
print (y["city"])

"""

f = open("pattern-1.json", "r")
#datax = json.loads(f)
#keyz = datax.keys()
#print keyz
#for i in f:
#for x in range(0,len(keyz)):
#  print(i)
data = json.load(f)
print data["city"]





"""
for i in range(0,len(keyz)):
    city = datax[keyz[i]]["city"]
    for cit in city:
        print cit

"""












