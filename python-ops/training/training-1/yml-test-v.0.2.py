import argparse
import yaml

def parseYml():

    arg=argparse.ArgumentParser(description="parse yml file")
    arg.add_argument("-i", "--ip", help="Extract ip of yml file")
    argument=arg.parse_args()
    if argument.ip:
        return argument.ip
""" 
def ip():
    try:
        arg=parseYml()  
        with open(arg) as stream:
            data=yaml.load(stream)
            for x, y in data.iteritems():
                print(str(y).strip("']["))
    except yaml.YAMLError as exc:
        print(exc)
ip()

"""
def fping(filex):
    ff = file(filex,'r')
    wh = yaml.load(ff)
    ips = []
    for ind in wh.values():
     for ip in ind:
      ips.append(ip)
      print ip

fping(parseYml())
