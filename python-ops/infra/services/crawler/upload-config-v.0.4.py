import requests
import subprocess
import json
import os
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning, SNIMissingWarning
# silence warnings in urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)

# for 6.6.5
cwd = os.getcwd()
def tokenv():
 with requests.session() as q:
  if os.path.exists("%s/temp.txt"%cwd) and os.path.getsize("%s/temp.txt"%cwd) > 0:
        fox=open("temp.txt","r+")
        apk= "%s"%fox.readline().rstrip(" ")
        log = q.get("https://app.searchstax.co/api/rest/v2/account/TDQ53Q02KT/deployment/",headers={"Authorization":apk})
        if "expired" or "invalid" not in log.text:
                all=json.loads(log.text)
                return all
                host=all["results"][0]["uid"]
                servs=all["results"][0]["servers"]
        else:
                fox.close()
                subprocess.Popen("rm temp.txt", shell=True, stdout=subprocess.PIPE)
                foo= open("temp.txt","w+")
                da={"username":"xxxxxxx","password":"xxxxxx"}
                fl = q.post("https://app.searchstax.co/api/rest/v1/obtain-auth-token/",data=da)
                tok = json.loads(fl.text)
                apk= "Token %s"%tok["token"]
                log = q.get("https://app.searchstax.co/api/rest/v2/account/TDQ53Q02KT/deployment/",headers={"Authorization":apk})
                if "expired" not in log.text:
                        foo.write(apk)
                        foo.close()
                        tokenv()
                else:
                        print "EXIT CODE 2"
  else:
        foo= open("temp.txt","w+")
        da={"username":"xxxxxxxx","password":"xxxxxx"}
        fl = q.post("https://app.searchstax.co/api/rest/v1/obtain-auth-token/",data=da)
        tok = json.loads(fl.text)
        apk= "Token %s"%tok["token"]
        log = q.get("https://app.searchstax.co/api/rest/v2/account/TDQ53Q02KT/deployment/",headers={"Authorization":apk})
        if "expired" not in log.text:
                foo.write(apk)
                foo.close()
                tokenv()
        else:
                print "EXIT CODE 2"

log = tokenv()
end = log["results"][0]["http_endpoint"]
linx = str(end).replace("https://","")
def solr6(path,nam):
	# 1. Uploading Solr Config to Zookeepers
                 
        print 'Uploading solr config'
        cmd = '/opt/zookeeper-1/bin/zkCli.sh -zkhost  %s:2181 -cmd upconfig -confdir %s -confname %s'%(linx.replace("/solr/",""),path,nam)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	out, err = p.communicate()
        print out

	# 2. Creating a collection
	#curl 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/admin/collections?action=CREATE&name=helloworld&collection.configName=test&numShards=3'

	url = '%s/admin/collections?action=CREATE&name=helloworld&collection.configName=test&numShards=3'%str(end)
	#headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.get(url,verify=False)
	print 'Creating a collection'
	print r.text

	# 3. Uploading data to a collection
	#curl	-X POST -H 'Content-type:application/json' -d @sample.json 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/helloworld/update?commit=true'
	

	url = '%s/helloworld/update?commit=true'%str(end)
	payload = json.loads(open("sample.json").read())
	headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.post(url, verify=False,data=payload, headers=headers)
	print 'Uploading data to a collection'
	print r.text
	# 4. Querying a collection
	# curl 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/helloworld/select?q=*:*&wt=json&indent=true'

	url = '%s/helloworld/update?commit=true'%str(end)
	headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.post(url, verify=False,data=payload, headers=headers)
	print 'Querying a collection'
	print r.text

# for 7.4
def solr7():


        # 1. Uploading Solr Config to Zookeepers
        #result = subprocess.run(['/opt/zookeeper/bin/zkcli.sh', '-zkhost localhost:2181 -cmd upconfig -confdir /opt/scripts/testcases/searchstax-client/solr-7/configsets -confname rahultestconfig'], stdout=subprocess.PIPE)
        #result = subprocess.run(['/opt/zookeeper/bin/zkcli.sh', '-zkhost ss276718-1-ap-northeast-1-aws.searchstax.com:2181 -cmd upconfig -confdir /opt/scripts/testcases/searchstax-client/solr-7/configsets -confname rahultestconfig'], stdout=subprocess.PIPE)
       #(out, err) = result.communicate()

	# 2. Creating a collection
	# curl 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/admin/collections?action=CREATE&name=hellorahul&collection.configName=rahultestconfig&numShards=1&replicationFactor=1&maxShardsPerNode=1' -k

	url = '%s/admin/collections?action=CREATE&name=hellorahul&collection.configName=rahultestconfig&numShards=1&replicationFactor=1&maxShardsPerNode=1'%str(end)
	#headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.get(url,verify=False)
	print 'Creating a collection'
	print r.text
	


       # 3.Uploading data to a collection

	url = '%s/hellorahul/update?commit=true'%str(end)
	payload = json.loads(open("sample.json").read())
	headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.post(url, verify=False,data=payload, headers=headers)
	print 'Uploading data to a collection'
	print r.text


	# 4. Querying a collection
	# curl 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/hellorahul/select?q=*:*&wt=json&indent=true' -k

	url = '%s/helloworld/update?commit=true'%str(end)
	headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.post(url, verify=False,data=payload, headers=headers)
	print 'Querying a collection'
	print r.text
if __name__ == '__main__':
	import argparse, sys
	parser = argparse.ArgumentParser(description='receive the info')
	parser.add_argument(dest='solr', nargs=1, type=str, help="receive if the info is solr6 or solr7")
	parser.add_argument('-c',nargs=2,type=str,help="path of the config file")
	parser.add_argument('-n',nargs=3,type=str,help="name of the config")
	if len(sys.argv) > 1:
		args = parser.parse_args([sys.argv[1]])
		config_file = args.solr
	else:
		args = parser.parse_args(['config.py'])
		config_file = args.solr
	config = __import__(config_file[0].split('.py')[0].split('/')[-1])
        current_env = config.Environment._current_env
	_config = None
	if current_env == 'test':
		_config = config.TestConfig._config
	elif current_env == 'qa':
		_config = config.QATestConfig._config
	elif current_env == 'prod':
		_config = config.ProdTestConfig._config
	else:
		raise(Exception("Current env not mapped in test, qa or prod"))
	
	if _config['solr_version'].startswith('6'):
		path = sys.argv[2]
		nam = sys.argv[3]
		solr6(path,nam)
	elif _config['solr_version'].startswith('7'):
		solr7()
	else:
		raise(Exception("Solr version not mapped in 6 or 7"))

