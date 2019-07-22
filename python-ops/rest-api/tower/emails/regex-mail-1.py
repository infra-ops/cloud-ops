import argparse,csv
from datetime import datetime

def start(fname):
	tempt= datetime.now()
	ffname= "%s.csv"%tempt.strftime("%d-%b-%Y (%H:%M:%S)")
	hosts=[]
	all = open(fname,"r+")
	data=all.readlines()
	del data[0:data.index("TASK [print out] ***************************************************************\n")]
	del data[0]
	del data[data.index("PLAY RECAP *********************************************************************\n"):len(data)-1]
	final = open(ffname,"a+")
	writer = csv.writer(final)
	writer.writerow(["HOSTNAMES","PACKAGES NAMES"])
	for i in data:
		if "ok: [" in i:
			temp = i.replace("ok: [","")
			host = temp.replace("] => {\n","")
			hosts.append(host)
	for host in hosts:
		modules=[]
		modules_final=[]
		ip="ok: [%s] => {\n"%host
		for i in range(0,len(data)):
				k=data[i]
				if k == ip:
					for l in range(i+1,len(data)):
						if "}\n" in data[l]:
							break
						else:
							modules.append(data[l])
		del modules[0]
		try:
			del modules[len(modules)-1]
			for k in modules:
				k=k.replace('", \n',"")
				k=k.replace('"        "',"")
				k=k.replace('        "',"")
				modules_final.append(k)
		except:
			pass
		try:
			writer.writerow([host,modules_final[0]])
			del modules_final[0]
		except:
			writer.writerow([host,""])
		for q in modules_final:
			writer.writerow(["",q])
parser = argparse.ArgumentParser()
parser.add_argument("-f")
args=parser.parse_args()
if (args.f is None):
	print "missing argument !"
	quit()
else:
	start(args.f)
