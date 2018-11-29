import subprocess
import argparse
from kubernetes import client, config


def create(act):
	#kubectl create -f kibana/nginx-deploy.yml
	p = subprocess.Popen("kubectl create -f %s"%act,shell=True, stdout=subprocess.PIPE)
	p.wait()
	out = p.communicate()
	print out[0]
def createn(act,nact):
        #kubectl create -f kibana/nginx-deploy.yml -n logging
        p = subprocess.Popen("kubectl create -f %s -n %s"%(act,nact),shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()
        print out[0]


def delete(pat):
	#kubectl delete -f
	#kubectl delete -f kibana/nginx-deploy.yml -n logging
	p = subprocess.Popen("kubectl delete -f %s"%pat,shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()
       	print out[0]


def pods(pods):
	#kubectl get pods -o wide -n logging
	p = subprocess.Popen("kubectl get pods -o wide",shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()
        print out[0]

def svc(svc):
	#kubectl get svc -o wide -n logging
        p = subprocess.Popen("kubectl get svc -o wide",shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()
        print out[0]

def logs(logs):
        #kubectl logs po/nginx -n logging
        p = subprocess.Popen("kubectl logs %s"%logs,shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()
        print out[0]
def desc(describe):
	#kubectl describe po/nginx
	p = subprocess.Popen("kubectl describe %s"%describe,shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()
        print out[0]
def main():
	    parser = argparse.ArgumentParser()
	    parser.add_argument("-c")
            parser.add_argument("-r")
            parser.add_argument("-l")
	    parser.add_argument("-ns")
            parser.add_argument("-d")
            parser.add_argument("-p")
            parser.add_argument("-s")
            args = parser.parse_args()
	    if (args.r is not None) and ((args.s and args.c and args.p and args.l and args.d) is None):
		delete(args.r)
	    elif ((args.c is not None)and(args.ns is None)) and ((args.s and args.r and args.p and args.l and args.d) is None):
		create(args.c)
	    elif (args.p is not None) and ((args.s and args.r and args.c and args.l and args.d) is None):
		pods(args.p)
	    elif (args.s is not None) and ((args.p and args.r and args.c and args.l and args.d) is None):
		svc(args.s)
	    elif (args.l is not None) and ((args.s and args.p and args.r and args.c and args.d) is None):
		logs(args.l)
	    elif (args.d is not None) and ((args.s and args.p and args.r and args.c and args.l) is None):
		desc(args.d)
	    elif ((args.c and args.ns) is not None) and ((args.s and args.p and args.r and args.d and args.l) is None):
		createn(args.c,args.ns)
main()
