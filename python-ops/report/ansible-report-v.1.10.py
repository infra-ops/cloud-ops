#!/usr/bin/python
#import modules
import argparse
import csv
import pandas as pd
import os
import re 
import subprocess
 

def gencsv(out):
	
	new_data=str(out.replace("msg: all out "," "))
	register=new_data.split("-")
	#new_data=str(out.replace("msg:allout"," "))

	#-------------------clear sample.csv to empy file
	sample=open("sample.csv", "w")
	sample.write("")
	sample.close()
	
	#----------extract info block 
	try:
		with open("sample.csv", "a") as fl:
			data=csv.writer(fl, delimiter=",")
			data.writerow(["IP","HOSTNAME","OS VERSION","CPU USAGE","MEMORY USAGE","ANSIBLE VERSION","NGINX STATUS","DB STATUS"])
			print("Output:\n\tPlease check sample.csv file in your current dir\n")
			for rowReg in register:
				dt=open("raw-data.csv", "a")     
				dt.write(str(rowReg).replace(" ",""))
				dt.close()
			with open("raw-data.csv", "r") as fl:
				csv_data=csv.reader(fl,delimiter=",")
                        	for row in csv_data:
					data.writerow([str(row[0]).replace("Ip",""),str(row[1]).replace("hostnames",""),str(row[2]).replace("os_version","").replace(" ","No"),str(row[3]).replace("cpu",""),str(row[4]).replace("mem",""),str(row[5]).replace("ansible",""),str(row[6]).replace("nginx",""),str(row[7]).replace("db","")])
					#print([str(row[0]).replace("Ip",""),str(row[1]).replace("hostnames",""),str(row[2]).replace("os_version",""),str(row[3]).replace("cpu",""),str(row[4]).replace("mem",""),str(row[5]).replace("ansible",""),str(row[6]).replace("nginx",""),str(row[7]).replace("db","")])
	
	finally:
		subprocess.Popen("rm -rf raw-data.csv", shell=True, stdout=subprocess.PIPE) #remove temporary file 
	

	#replacing NaN value with No
        rData=pd.read_csv("sample.csv", index_col="IP")
        rData=rData.fillna("NO")
	rData["DB STATUS"].replace("\.0", "", regex=True, inplace=True)
	print(rData)
        rData.to_csv("sample.csv", sep=",", encoding="utf-8")


def execute(fur,sur):
	cmd2 = "ansible-playbook -i %s %s"%(fur,sur)
	p=subprocess.Popen("%s|awk '/all out Ip/ {print $0}'"%(cmd2), stdout=subprocess.PIPE, shell=True)
	out,err= p.communicate()
        return out

if __name__ == '__main__':
        parser = argparse.ArgumentParser()
        parser.add_argument("-i")
        parser.add_argument("-f")
        args = parser.parse_args()
        if (args.i is not None) and (args.f is not None):
                out = execute(args.i,args.f)
                gencsv(out)
        else:
                print("Missing arguments .")

