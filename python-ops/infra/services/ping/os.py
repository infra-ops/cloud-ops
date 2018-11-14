##execution process
###python ping.py -i 127.0.0.1
###python ping.py -l ping-ips.yml
import datetime
import yaml
import subprocess
import argparse
import csv

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

try:
    import yaml
except ImportError as ie:
    LIB_MAP = {'yaml': 'PyYAML'}
    m = ie.message
    missing_mod = m[m.rfind(" "):].strip()
    msg = "missing python module '%s' (please install manually)\n" % missing_mod\
        + "  use: pip install %s" % LIB_MAP.get(missing_mod, missing_mod)
    error(msg)

#arg = sys.argv[1]

def sping(oip):
	p = subprocess.Popen("ping -c 1 %s"%oip,shell=True, stdout=subprocess.PIPE)
	p.wait()
	out = p.communicate()
	reponse = p.returncode
	if "ttl=64" in str(out[0]):
		print "%s is linux"%oip
		fo.writerow(["%s"%oip,"Linux"])
	else:
		fo.writerow(["%s"%oip,"Windows"])
		print "%s is reachable"%oip

def fping(filex):
    ff = file(filex,'r')
    wh = yaml.load(ff)
    ips = []
    for ind in wh.values():
     for ip in ind:
      ips.append(ip)
    for i in ips:
        sping(i)

def main():
            fo.writerow(['IP', 'OS'])
	    parser = argparse.ArgumentParser()
	    parser.add_argument("-i")
	    parser.add_argument("-l")
	    args = parser.parse_args()
	    if (args.i is not None) and (args.l is None):
	      sping(args.i)
	    elif (args.i is None) and (args.l is not None):
	      fping(args.l)
	    else:
	      print "Wrong paramter combination ."
csv_file= open('ip-status-%s.csv'%current_time_string, mode='w')
fo = csv.writer(csv_file,delimiter=',')
main()
