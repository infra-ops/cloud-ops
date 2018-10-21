#!/usr/bin/python

import subprocess
import re

port = 80

cmd = 'netstat -ntlp | grep "%s"' % port
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
out, _ = p.communicate()

matches = re.findall("^[\w\d\s\.:]+:(%s)\s+.*$" % port, out, re.MULTILINE)
print matches[0] if matches else "port '%s' is not in use" % port
