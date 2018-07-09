#!/usr/bin/python

import argparse
import re
import subprocess
import sys

import yaml


def is_port_used(port):
    cmd = 'netstat -ntlp | grep "%s"' % port
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, _ = p.communicate()

    matches = re.findall("^[\w\d\s\.:]+:(%s)\s+.*$" % port, out, re.MULTILINE)
    return True if matches else False


def main():
    parser = argparse.ArgumentParser(description="testing")
    parser.add_argument('-p', '--port', dest='port', default='80', help='port to check')
    args = parser.parse_args()

    try:
        port = int(args.port)
    except ValueError:
        print "ERROR: invalid port '%s' (must be a number)"
        sys.exit(-1)

    if is_port_used(args.port):
        print "ok"
    else:
        print "not ok"


if __name__ == '__main__':
    main()
