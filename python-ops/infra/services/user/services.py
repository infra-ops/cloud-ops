import subprocess
import argparse
import yaml


def cmd():
       nginx_status = "service nginx status"
       nginx_ps     = "ps -ef | grep nginx"
       return nginx_status,nginx_ps

def run():
    for cmds in cmd():
                dat = []
		p = subprocess.Popen(cmds ,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
		out, err=p.communicate()
		dat.append(out)
		for dt in dat:
			print("%s\n" %(dt))

def main():
    rn=run()
    rn

main()
