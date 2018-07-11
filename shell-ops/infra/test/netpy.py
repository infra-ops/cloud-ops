import sys
import socket
import time

host = sys.argv[1]
port = int(sys.argv[2])
# type => ["tcp" or "udp"]
type = sys.argv[3]
test = ""
if len(sys.argv) > 4 :
test = sys.argv[4]

while 1 :
if type == "udp":
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
else:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
try:
if type == "udp":
s.sendto("--TEST LINE--", (host, port))
recv, svr = s.recvfrom(255)
s.shutdown(2)
print "Success connecting to " + host + " on UDP port: " + str(port)
else:
s.connect((host, port))
s.shutdown(2)
print "Success connecting to " + host + " on TCP port: " + str(port)
except Exception, e:
try:
errno, errtxt = e
except ValueError:
print "Cannot connect to " + host + " on port: " + str(port)
else:
if errno == 107:
print "Success connecting to " + host + " on UDP port: " + str(port)
else:
print "Cannot connect to " + host + " on port: " + str(port)
print e
if test != "C" :
sys.exit(0)

s.close
time.sleep(1)
