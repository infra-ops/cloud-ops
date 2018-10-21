import sys
import urllib2
import re





arg = sys.argv[1]

def runfile(arg):
    f1 = open(arg, 'r')

    a = f1.readlines()
    urls = [url.strip() for url in a ]

    for i in urls:
        try:
            a = urllib2.urlopen(i)
            source = a.read()
            pat = '\d{9}'
            phone = re.findall(pat, source)
            print phone
        except:
            pass

    f1.close()


runfile(arg)
