import yaml
import yamlordereddictloader

"""
with open("ecs.yml", 'r') as stream:
    try:
        print(yaml.load(stream))
    except yaml.YAMLError as exc:
        #print(exc)
        #print "dict['us-east-1']: ", dict['us-east-1']
        for exc in ip:
            print ip["us-east-1"]




"""
"""
def ip():
    ff = file(ecs.yml,'r')
    wh = yaml.load(ff)
    ips = []
    for ind in wh.values():
     for ip in ind:
      ips.append(ip)

ip()
"""



"""

 
def ip():
    try:
        with open("ecs.yml") as stream:
            data=yaml.load(stream)
            location=["east","west"]
            for value in data["us-east-1"]:
                print(value)
    except yaml.YAMLError as exc:
        print(exc)
ip()

"""

def ip():
    try:
        with open("ecs.yml") as stream:
            data=yaml.load(stream)
            location=["us-east-1","us-west-1"]
            for x in location:
                for value in data[x]:
                    print(value)
    except yaml.YAMLError as exc:
        print(exc)
ip()





""" 
with open("ecs.yml") as f:
    yaml_data = yaml.load(f, Loader=yamlordereddictloader.Loader)
    print(yaml_data)

"""
