#!/usr/bin/python
#python security-check-8.py  -i /etc/ansible/inventories/generic/static/local/local.yml -f /etc/ansible/playbooks/patchman/log-check.yml
import re
import json
from datetime import datetime as dt
import subprocess
import argparse
import csv
def gencsv(out):
		with open("out1000.csv","w+") as temp:
			temp.write("IP, Node ID , Logs being stored in /opt/data/ , Solr log path ,ZK logs path\n")
			ips = []
			nid = []
			out = out.decode("utf-8")
			print(out)
			xx = out.split("\n")
			for nli in xx:
				if "ansible_default_ipv4.address" in nli:
					ipx=nli.split(":")[1]
					ips.append(ipx.replace('"',''))
			for line in xx:
				if "ansible_nodename" in line:
					node = line.split(":")[1]
					nid.append(node.replace('"',''))
			out= out.replace("\n","")
			for hs in nid:
					optx='ok: [%s] => {    "msg": "log data path : /opt/data"}'%hs.replace(" ","")
					solx='ok: [%s] => {    "msg": "Solr logs path: /opt/data/solr/logs"}'%hs.replace(" ","")
					zkx='ok: [%s] => {    "msg": "Zookeeper log path: /opt/data/zookeeper/logs"}'%hs.replace(" ","")
					ipx = ips[int(nid.index(hs))]
					opt = ""
					sol = ""
					zk = ""
					if optx in out:
						opt = "/opt/data"
					else:
						opt = "NA"
					if solx in out:
						sol = "Data present under /opt/data/solr/logs"
					else:
						sol = "NA"
					if zkx in out:
						zk = "Data present under /opt/data/zookeeper/logs"
					else:
						zk = "NA"
					temp.write("%s,%s,%s,%s,%s\n"%(ipx,hs,opt,sol,zk))
def execute(fur,sur):
		cmd2 = "ansible-playbook -i %s %s"%(fur,sur)
		p = subprocess.Popen(cmd2, stdout=subprocess.PIPE, shell=True)  
		out, err = p.communicate()
		return(out)
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
