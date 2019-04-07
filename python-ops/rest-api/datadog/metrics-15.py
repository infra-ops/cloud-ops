import sys,os
import json
from datetime import datetime as dt
from datadog import initialize, api
import datadog
import argparse
import requests.packages.urllib3
import requests

options = {
		'api_key': 'd8f6a0cc9b74872e66712b35d4825742',
		'app_key': '849d9f1081bd518718109162d30fe9774ffac264'
}

initialize(**options)

def delete_monitor(monitor_ids):

	log_content = []

	log_content.append("[{0}] Initialized the process.".format(dt.now().isoformat()))

	for monitor_id in monitor_ids:
		try:
			res=api.Monitor.delete(monitor_id)
			log_content.append("Deleted metric for monitor id {0}".format(monitor_id))
		except Exception as exception:
			log_content.append("Failed to delete metric for monitor id {0}".format(monitor_id))
			#log_content.append("Exception message: {0}".format(exception))

	log_content.append("[{0}] Finished the process.".format(dt.now().isoformat()))

	content = "\n".join(log_content)

	print(content)
	upload_content_to_s3("dev-dd-4",content)

def upload_content_to_s3(bucket, content):
	import boto3
	client = boto3.client('s3')
	client.put_object(
		Bucket=bucket,
		Key="logs/{0}.log".format(dt.now().isoformat()[:-10]),
		Body=content
	)

def create_monitor(json_file, received_host):
	# Create a cpu2 monitor
	instances = json_file if json_file != None else {'hosts': []}
	log_content = []

	log_content.append("[{0}] Initialized the process.".format(dt.now().isoformat()))

	#cpu
	options1 = {
		"timeout_h": 1,
		"notify_no_data": False,
		"notify_audit": True,
		"require_full_window": True,
		"new_host_delay": 300,
		"include_tags": False,
		"escalation_message": "",
		"locked": False,
		"renotify_interval": "0",
		"evaluation_delay": "",
		"thresholds": {
			"critical": 80
		}
	}

	#memory
	options2 = {
		"timeout_h": 1,
		"notify_no_data": False,
		"notify_audit": True,
		"require_full_window": True,
		"new_host_delay": 300,
		"include_tags": False,
		"escalation_message": "",
		"locked": False,
		"renotify_interval": 10,
		"evaluation_delay": "",
		"thresholds": {
			"critical": 0.2
		}
	}

	#disk
	options3 = {
		"timeout_h": 1,
		"notify_no_data": False,
		"notify_audit": True,
		"require_full_window": True,
		"new_host_delay": 300,
		"include_tags": False,
		"escalation_message": "",
		"locked": False,
		"renotify_interval": 10,
		"evaluation_delay": "",
		"thresholds": {
			"critical": 78000000000
		}
	}

	tags = ["app:INFRA"]

	if received_host != None:
		#cpu
		try:
			res= api.Monitor.create(
				type="metric alert",
				query="avg(last_5m):avg:aws.ec2.cpuutilization{"+ received_host +"} > 80",
				name=received_host +" CPU Usage 2 > 80%",
				message="@sudipta@searchstax.com",
				tags=tags,
				options=options1
			)
			id = res['id']
			log_content.append("CPU Metric created on {0} {1}".format(received_host, id))
		except:
			log_content.append("CPU Metric failed on {0}".format(received_host))

		#memory
		try:
			res=api.Monitor.create(
				type="metric alert",
				query="avg(last_5m):avg:system.mem.pct_usable{"+ received_host +"} <= 0.2",
				name=received_host + " MEMORY Usage 2 < 20%",
				message="@sudipta@searchstax.com",
				tags=tags,
				options=options2
			)
			id = res['id']
			log_content.append("Memory Metric created on {0} {1}".format(received_host, id))
		except:
			log_content.append("Memory Metric failed on {0}".format(received_host))

		#disk
		try:
			res=api.Monitor.create(
				type="metric alert",
				query="avg(last_5m):avg:system.disk.used{"+received_host+"} by {device} > 78000000000",
				name=received_host + " DISK Usage 2 < 20%",
				message="@sudipta@searchstax.com",
				tags=tags,
				options=options3
			)
			id = res['id']
			log_content.append("Disk Metric created on {0} {1}".format(received_host, id))
		except:
			log_content.append("Disk Metric failed on {0}".format(received_host))

	for host in instances['hosts']:
		#cpu
		try:
			res= api.Monitor.create(
					type="metric alert",
					query="avg(last_5m):avg:aws.ec2.cpuutilization{"+host['query']+"} > 80",
					name=host['name'] +" CPU Usage 2 > 80%",
					message="@sudipta@searchstax.com",
					tags=tags,
					options=options1
			)
			id = res['id']
			log_content.append("CPU Metric created on {0} {1}".format(host['name'], id))
		except:
			log_content.append("CPU Metric failed on {0}".format(host['name']))

		#memory
		try:
			res=api.Monitor.create(
				type="metric alert",
				query="avg(last_5m):avg:system.mem.pct_usable{"+host['query']+"} <= 0.2",
				name=host["name"]+" MEMORY Usage 2 < 20%",
				message="@sudipta@searchstax.com",
				tags=tags,
				options=options2
			)
			id = res['id']
			log_content.append("Memory Metric created on {0} {1}".format(host['name'], id))
		except:
			log_content.append("Memory Metric failed on {0}".format(host['name']))

		#disk
		try:
			res=api.Monitor.create(
				type="metric alert",
				query="avg(last_5m):avg:system.disk.used{"+host['query']+"} by {device} > 78000000000",
				name=host["name"]+" DISK Usage 2 < 20%",
				message="@sudipta@searchstax.com",
				tags=tags,
				options=options3
			)
			id = res['id']
			log_content.append("Disk Metric created on {0} {1}".format(host['name'], id))
		except:
			log_content.append("Disk Metric failed on {0}".format(host['name']))

	log_content.append("[{0}] Finished the process.".format(dt.now().isoformat()))

	content = "\n".join(log_content)
	upload_content_to_s3("dev-dd-4",content)
	print content

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Receive the input file directory.')
	parser.add_argument("-f",dest="input_file", metavar='N', type=str, help="The directory of the input file")
	parser.add_argument("-k",dest="delete_file", metavar='N', type=str, help="The directory of the input file for delete")
	parser.add_argument("-d", dest='monitor_id', nargs="*", help="The monitor id to delete")
	parser.add_argument("-n", dest='host', nargs="?", help="The monitor id to delete")

	args = parser.parse_args()
	if (args.monitor_id is not None and len(args.monitor_id) is not 0) or args.delete_file != None:
		ids = args.monitor_id if args.monitor_id != None else []
		if args.delete_file != None:
			file = open(args.delete_file)
			content = file.read()
			content_ids = content.split('\r\n') if '\r\n' in content else content.split('\n')
			ids += content_ids
		delete_monitor(ids)
	else:
		json_file, host = None, None
		if args.input_file is not None:
			file = open(args.input_file)
			json_file = json.loads(file.read())
		
		host = args.host
		
		create_monitor(json_file, host)
    
