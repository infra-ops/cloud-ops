#!/usr/bin/python

import subprocess
import re
import argparse
import yaml


parser = argparse.ArgumentParser(description="testing")
parser.add_argument('-p', '--port', dest='port', default='80', help='port scanning')
args = parser.parse_args()


port_list = args.port



def is_port_used(port):
    cmd = 'netstat -ntlp | grep "%s"' % port
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, _ = p.communicate()

    matches = re.findall("^[\w\d\s\.:]+:(%s)\s+.*$" % port, out, re.MULTILINE)
    return True if matches else False

if is_port_used(80):
    print "ok"
else:
    print "not ok"
