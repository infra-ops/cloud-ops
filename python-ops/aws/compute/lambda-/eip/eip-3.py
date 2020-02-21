import sys,os
import json
from datetime import datetime as dt
import boto3

eip_region = "us-east-1"

#upload log the bucket
def upload_content_to_s3(bucket, content):
	import boto3
	client = boto3.client('s3')
	client.put_object(
		Bucket=bucket,
		Key="logs/{0}.log".format(dt.now().isoformat()[:-10]),
		Body=content
	)

def release_eip(json_file, eip_list):
	log_content = []
	log_content.append("[{0}] Initialized the process.".format(dt.now().isoformat()))
	
	if json_file is None:
		json_file = {}
	
	if eip_list != None:
		for eip in eip_list:
			try:
				client = boto3.client('ec2', eip_region)
				client.release_address(AllocationId=eip)
				log_content.append("Released IP {}".format(eip))
			except Exception as exception:
				log_content.append("Failure to release IP {}".format(eip))
				log_content.append("Exception: {}".format(exception))
	
	for region in json_file.keys():
		client = boto3.client('ec2', region)
		for eip in json_file[region]:
			try:
				client.release_address(AllocationId=eip)
				log_content.append("Released IP {}".format(eip))
			except Exception as exception:
				log_content.append("Failure to release IP {}".format(eip))
				log_content.append("Exception: {}".format(exception))

	log_content.append("[{0}] Ended the process.".format(dt.now().isoformat()))
	content = "\n".join(log_content)
	upload_content_to_s3("dev-log-4",content)
	print content

if __name__ == '__main__':
	import argparse
	
	parser = argparse.ArgumentParser(description='Receive the input file directory.')
	parser.add_argument("-f", dest="input_file", metavar='N', type=str, help="file contains eips which are need to be released")
	parser.add_argument("-i", dest='eip', nargs="*", help="eip to releases")
	parser.add_argument("-r", dest='region', nargs="?", help="eip to releases")

	args = parser.parse_args()
	json_file, eip = None, None
	
	if args.region is not None:
		eip_region = args.region
	
	try:
		file = open(args.input_file)
		json_file = json.loads(file.read())
	except:
		pass
	eip = args.eip
	release_eip(json_file, eip)

def lambda_handler(event, context):
	release_eip(event, None)

