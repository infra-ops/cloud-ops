import requests
import subprocess
import json

# for 6.6.5


def solr6():
	# 1. Uploading Solr Config to Zookeepers
	#result = subprocess.run(['/opt/zookeeper-1/bin/zkcli.sh', '-zkhost localhost:2181 -cmd upconfig -confdir /opt/scripts/testcases/searchstax-client/solr-6/configsets/basic_configs/conf/ -confname test'], stdout=subprocess.PIPE)

	# 2. Creating a collection
	#curl 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/admin/collections?action=CREATE&name=helloworld&collection.configName=test&numShards=3'

	url = 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/admin/collections?action=CREATE&name=helloworld&collection.configName=test&numShards=3'
	#headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.get(url)
	print 'Creating a collection'
	print r.text

	# 3. Uploading data to a collection
	#curl	-X POST -H 'Content-type:application/json' -d @sample.json 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/helloworld/update?commit=true'
	

	url = 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/helloworld/update?commit=true'
	payload = json.loads(open("sample.json").read())
	headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.post(url, data=payload, headers=headers)
	print 'Uploading data to a collection'
	print r.text
	# 4. Querying a collection
	# curl 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/helloworld/select?q=*:*&wt=json&indent=true'

	url = 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/helloworld/update?commit=true'
	headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.post(url, data=payload, headers=headers)
	print 'Querying a collection'
	print r.text

# for 7.4
def solr7():
        # 1. Uploading Solr Config to Zookeepers
        #result = subprocess.run(['/opt/zookeeper/bin/zkcli.sh', '-zkhost localhost:2181 -cmd upconfig -confdir /opt/scripts/testcases/searchstax-client/solr-7/configsets -confname rahultestconfig'], stdout=subprocess.PIPE)

	# 2. Creating a collection
	# curl 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/admin/collections?action=CREATE&name=hellorahul&collection.configName=rahultestconfig&numShards=1&replicationFactor=1&maxShardsPerNode=1' -k

	#url = 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/helloworld/update?commit=true'
	url = 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/admin/collections?action=CREATE&name=hellorahul&collection.configName=rahultestconfig&numShards=1&replicationFactor=1&maxShardsPerNode=1'
	#headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.get(url)
	print 'Creating a collection'
	print r.text
	# 3.Uploading data to a collection

	url = 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/hellorahul/update?commit=true'
	payload = json.loads(open("sample.json").read())
	headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.post(url, data=payload, headers=headers)
	print 'Uploading data to a collection'
	print r.text
	# 4. Querying a collection
	# curl 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/hellorahul/select?q=*:*&wt=json&indent=true' -k

	url = 'https://ss276718-ap-northeast-1-aws.searchstax.com/solr/helloworld/update?commit=true'
	headers = {'Content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
	r = requests.post(url, data=payload, headers=headers)
	print 'Querying a collection'
	print r.text
if __name__ == '__main__':
	import argparse, sys
	parser = argparse.ArgumentParser(description='receive the info')
	parser.add_argument(dest='solr', nargs=1, type=str, help="receive if the info is solr6 or solr7")
	
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
		solr6()
	elif _config['solr_version'].startswith('7'):
		solr7()
	else:
		raise(Exception("Solr version not mapped in 6 or 7"))
