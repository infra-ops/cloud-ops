import json

f = open("nodes-5.json", "r")
datax = json.load(f)
keyz = datax.keys()
#print data
for i in range(0,len(keyz)):
    try:
           hosts = datax[keyz[i]]["hosts"]
           user = datax[keyz[i]]["vars"]["ansible_ssh_user"]
           psw = datax[keyz[i]]["vars"]["ansible_ssh_pass"]
           for ip in hosts:
              print ip
              print user
              print psw
    except Exception as e:
                        continue


