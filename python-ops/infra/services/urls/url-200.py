#python url.py -u http://3.92.18.125
#python url.py -f links.yml

import requests
from requests.exceptions import RequestException
import argparse
import yaml




def check_url(url):
	try:
	   r=requests.get(url, verify=False)
	   if r.status_code == requests.status_codes.codes.ok:
	   	print("%s %s ok" %(url, r.status_code))


        except RequestException as error:
                print("%s is not reachable\n%s"%(url, error))
	



def check_url_file(yml):

	ipYml=open(yml,"r")
	urls=yaml.load(ipYml)	

	try:
	      for url in urls.values():	
		       r=requests.get(url, verify=False)
		       if r.status_code == requests.status_codes.codes.ok:
		       	print("%s %s ok" %(url, r.status_code))
			

	except RequestException as error:
		print("%s is not reachable\n%s"%(url, error))
		
		


def main():
	    parser = argparse.ArgumentParser(description="Parse yml ip list and get their header")
	    group=parser.add_mutually_exclusive_group()
	    group.add_argument("-y", "--yml")
            group.add_argument("-u", "--url")
	    args = parser.parse_args()
	    if args.yml:
	      check_url_file(args.yml)
	    elif args.url:
	      check_url(args.url)
	    else:
	      print "Wrong parameter combination ."

main()

