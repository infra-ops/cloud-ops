import pyAesCrypt
import argparse
def file_encrypt(password,file):
	bufferSize = 64 * 1024
	pyAesCrypt.encryptFile(file, "%s.aes"%file, password, bufferSize)
#what the hell is happening :o
parser = argparse.ArgumentParser()
parser.add_argument("-e")
parser.add_argument("-f")
parser.add_argument("-p")
args = parser.parse_args()
if (args.f is not None) and (args.p is not None):
	file_encrypt(args.p,args.f)
else:
	print "Missing argument"
