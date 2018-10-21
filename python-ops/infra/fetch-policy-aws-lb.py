import json,argparse
import subprocess,datetime
parser = argparse.ArgumentParser()
parser.add_argument('-l',type=str)
parser.add_argument('-f',type=str)
args = parser.parse_args()
flb= args.f
fin = args.l

if (flb is not None) and (fin is None):
	toem = open(flb,"r+")
	now = datetime.datetime.now()
	out = open("%s-%s-%s-%s-%s-%s-output.log"%(now.year,now.month,now.day,now.hour,now.minute,now.second),"a+")
	for clb in toem:
		clb = clb.rstrip("\n")
		comm = "aws elb describe-load-balancer-policies --load-balancer-name %s > %s-lb.json"%(clb,clb)
		process = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
		process.wait()
		with open("%s-lb.json"%clb,"r+") as foo:
			data = json.load(foo)
		dicl=data["PolicyDescriptions"][0]["PolicyAttributeDescriptions"]
		out.write("lb:%s\n"%clb)
		print "lb:%s"%clb
		for i in range(0,len(dicl)):
			if dicl[i]["AttributeValue"] == "true":
				out.write("%s\n"%dicl[i]["AttributeName"])
				print "%s"%dicl[i]["AttributeName"]
			else:
				continue
elif (flb is None) and (fin is not None):
                comm = "aws elb describe-load-balancer-policies --load-balancer-name %s > %s-lb.json"%(fin,fin)
                process = subprocess.Popen(comm, shell=True, stdout=subprocess.PIPE)
                process.wait()
                out = open("%s-output.log"%fin,"a+")
                with open("%s-lb.json"%fin,"r+") as foo:
                        data = json.load(foo)
                dicl=data["PolicyDescriptions"][0]["PolicyAttributeDescriptions"]
                for i in range(0,len(dicl)):
                        if dicl[i]["AttributeValue"] == "true":
                                out.write("%s\n"%dicl[i]["AttributeName"])
                                print "%s"%dicl[i]["AttributeName"]
                        else:
                                continue

