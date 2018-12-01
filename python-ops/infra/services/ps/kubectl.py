import subprocess
import argparse
from kubernetes import client, config


def create(act):
	#kubectl create -f
	p = subprocess.Popen("kubectl create -f %s"%act,shell=True, stdout=subprocess.PIPE)
	p.wait()
	out = p.communicate()
	print out[0]


def delete(pat):
	#kubectl delete -f
	#kubectl delete -f kibana/nginx-deploy.yml
	p = subprocess.Popen("kubectl delete -f %s"%pat,shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()
       	print out[0]


def pods(pods):
	#kubectl get pods -o wide
	p = subprocess.Popen("kubectl get pods -o wide",shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()
        print out[0]

def svc(svc):
	#kubectl get svc -o wide
        p = subprocess.Popen("kubectl get svc -o wide",shell=True, stdout=subprocess.PIPE)
        p.wait()
        out = p.communicate()
        print out[0]

def logs(logs):
        #kubectl logs po/nginx
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
            parser.add_argument("-d")
            parser.add_argument("-p")
            parser.add_argument("-s")
            args = parser.parse_args()
	    if (args.r is not None) and ((args.s and args.c and args.p and args.l and args.d) is None):
		delete(args.r)
	    elif (args.c is not None) and ((args.s and args.r and args.p and args.l and args.d) is None):
		create(args.c)
	    elif (args.p is not None) and ((args.s and args.r and args.c and args.l and args.d) is None):
		pods(args.p)
	    elif (args.s is not None) and ((args.p and args.r and args.c and args.l and args.d) is None):
		svc(args.s)
	    elif (args.l is not None) and ((args.s and args.p and args.r and args.c and args.d) is None):
		logs(args.l)
	    elif (args.d is not None) and ((args.s and args.p and args.r and args.c and args.l) is None):
		desc(args.d)
main()
