#!/usr/bin/python

import subprocess
import re

cmd = 'netstat -ntlp | grep "80"'

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
out, err = p.communicate()

found = False
for n in out.splitlines():
    result = re.split("\s+", n)
    if result and len(result) >= 4 and result[3].endswith(":80"):
        found = True
        break

if found:
    print "ok"
else:
    print "not ok"
