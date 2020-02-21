#execution process
#python s3.py -c /home/ubuntu/test/test.txt -b dev-dd-4
#python s3.py -c /home/ubuntu/test/*.sh -b dev-dd-4
#python s3.py -f upload.json

import os
import glob
from datetime import datetime as dt
import json
import boto3
import subprocess

def filesize(file):
	cmd = 'du -h {}'.format(file)
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	out, err = p.communicate()
	return out.strip()

def upload_content_to_s3(bucket, files):
	files = glob.glob(files)
	log_content = []
	for file in files:
		content = open(file).read()
		client = boto3.client('s3')
		client.put_object(
			Bucket=bucket,
			Key=file,
			Body=content
		)
		log_content.append('{} uploading to {}'.format(filesize(file), bucket))
	return log_content

def download_content_to_host(bucket):
	s3 = boto3.resource('s3')
	bucket = s3.Bucket(bucket)
	log_content = []
	for object in bucket.objects.all():
		bucket.download_file(object.key, os.path.join(os.curdir, object.key))
		#file_size = os.path.getsize(os.path.join(os.curdir, object.key))
		file = os.path.join(os.curdir, object.key)
		log_content.append('{} downloaded from {}'.format(filesize(file), bucket.name))
	return log_content

def process (bucketu, bucketd, file, json_file):
	log_content = []
	log_content.append("Script started at {}".format(dt.now().isoformat().replace("T", " ")[:-7]))
	if bucketd is not None:
		log_content += download_content_to_host(bucketd)
	if bucketu is not None and file is not None:
		log_content += upload_content_to_s3(bucketu, file)	
	if json_file is not None:
		data = json.loads(open(json_file).read())
		sources = []
		dest    = None
		for key in data.keys():
			if key.startswith("source"):
				sources.append(data[key])
			else:
				dest = data[key]
		for source in sources:
			log_content += upload_content_to_s3(dest, source)
	log_content.append("Script finished at {}".format(dt.now().isoformat().replace("T", " ")[:-7]))
	print "\n".join(log_content)
	file = open('{}.log'.format(dt.now().isoformat()[:-10].replace('T', '-').replace(':', '-')), 'wb')
	file.write("\n".join(log_content))
	file.close()

if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Receive the input file directory.')
	parser.add_argument("-s", dest="bucketd", nargs="?", type=str, help="bucket to download")
	parser.add_argument("-c", dest='file', nargs="?", help="file yo upload")
	parser.add_argument("-b", dest='bucketu', nargs="?", help="bucket and keys to upload")
	parser.add_argument("-f", dest='json_file', nargs="?", help="json file")

	args = parser.parse_args()
	process(args.bucketu, args.bucketd, args.file, args.json_file)
