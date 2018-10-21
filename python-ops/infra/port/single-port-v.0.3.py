import subprocess
import re

cmd = 'netstat -ntlp | grep "%s"' % 80
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
(out, err) = p.communicate()
#print out
matches = re.findall("^[\w\s\d\.]+:(%s)\s+.*$" % 80, out, re.MULTILINE)

if len(matches) != 0 and matches [0] == '80':
    print 'ok'
else:
    print 'not ok'
