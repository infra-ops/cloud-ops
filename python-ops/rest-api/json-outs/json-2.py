#!/usr/bin/python

import json


f = open("cf.json", "r")
data = json.load(f)
#print data["city"]
alldata= data["Mappings"]["SubnetConfig"]
netnames = alldata.keys()
cidr = []
for i in netnames:
	print "%s %s"%(i,alldata[i]["CIDR"])
