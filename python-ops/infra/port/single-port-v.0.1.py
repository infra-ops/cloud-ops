import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
r = s.connect_ex(('127.0.0.1',80))
if r == 0:
   print "port is open"
else:
   print "port is not open"
