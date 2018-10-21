#!/usr/bin/python
import subprocess
import re
import argparse
import yaml
import sys

def error(msg):
    print "ERROR: %s" % msg
    sys.exit(-1)


def is_port_used(port):
    cmd = 'netstat -ntlp | grep "%s"' % port
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    out, _ = p.communicate()
    matches = re.findall("^[\w\d\s\.:]+:(%s)\s+.*$" % port, out, re.MULTILINE)
    return True if matches else False


def main():
    parser = argparse.ArgumentParser(description="testing")
    parser.add_argument('-p', '--port', dest='port', help='port to scan')
    parser.add_argument('-f', '--portfile', dest='portfile', help='yaml file with ports to scan')

    args = parser.parse_args()
    port_list = []

    if args.port and args.portfile:
        error("Only specify ports to check via command line parameter '-p' OR yaml file '-f' (not both)")
    elif not args.port and not args.portfile:
        port_list = [80]  # default
    elif args.port:
        try:
            port_list = [int(args.port)]
        except ValueError:
            error("invalid port '%s' (must be an integer)" % args.port)
    elif args.portfile:
        try:
            with open(args.portfile) as stream:
                port_list = [entry['port'] for entry in yaml.load(stream)]
        except yaml.YAMLError as err:
            error("Could not load yaml port file '%s': %s" % (args.portfile, err))

    for port in port_list:
        if is_port_used(port):
            print "[%s] ok" % port
        else:
            print "[%s] not ok" % port

if __name__ == '__main__':
    main()
