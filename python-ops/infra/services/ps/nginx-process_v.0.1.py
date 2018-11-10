import re
import subprocess


cmd = 'ps -ef | pgrep {0}'.format('nginx')
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
(out, err) = p.communicate()
#print out
if out is not None and out is not '':
    print 'ok'
else:
    print 'not ok'
