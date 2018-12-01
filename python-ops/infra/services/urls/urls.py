#execution process
#python urls.py -u http://10.233.119.203/

#for i in {1..1000};do curl -I http://10.233.119.203/;done


import requests
import argparse







def check_url(url):
	try:
		for i in range(1,1001):
			r=requests.get(url)
			print "HTTP/1.1 %s %s"%(r.status_code,r.reason)
	except:
		print "%s is not reachable"%url
def main():
	    parser = argparse.ArgumentParser()
	    parser.add_argument("-u")
	    args = parser.parse_args()
	    if (args.u is not None) and ("http" in args.u):
	      check_url(args.u)
	    else:
	      print "Wrong paramter combination ."

main()


