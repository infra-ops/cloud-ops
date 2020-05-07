import boto3
import requests
import datetime
import sys
import json
import csv
import argparse
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart

log_file = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M") + "-start_stop.log"
regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ca-central-1', 
           'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 
           'ap-northeast-1', 'ap-northeast-2', 'ap-southeast-1', 
           'ap-southeast-2', 'ap-south-1', 'sa-east-1']

def sendLogFileEmail(log_data, log_data_csv):
	message = MIMEMultipart()
	message['Subject'] = log_file
	message['From'] = 'chakraborty.rock@gmail.com'
	message['To'] = 'sudipta1436@gmail.com'
	message.preamble = 'Multipart message.\n'
	message.attach(MIMEText('status of service'))	
	part = MIMEApplication(log_data)
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % log_file)
	partcsv = MIMEApplication(log_data_csv)
	log_file_csv = log_file.replace(".log", ".csv")
	partcsv.add_header('Content-Disposition', f'attachment; filename="{log_file_csv}"')
	#message.attach(part)
	message.attach(partcsv)
	client = boto3.client('ses')
	client.send_raw_email (
		Source='chakraborty.rock@gmail.com',
		Destinations=['sudipta1436@gmail.com'],
		RawMessage={'Data': message.as_string()}
	)
	#print "E-mail sent: " + str(response)

def arrayToString(x):
	if len(x) == 1:
		return x[0]
	else:
		return x[0] + ", " + arrayToString(x[1:])

##starting lambda function 





def lambda_handler(event, context):
	command = event["command"]
	#log_bucket = event["log-bucket"]
	instances = event["instances"]
	#s3 = boto3.resource('s3')
	log_data = ""
	log_data_csv = "regions, instance_id, status\n"
    ###printing start time
    
	if command.lower() == "start":
		log_data = log_data + "Start command started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print("Start command started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        
		## looping regions from list
        
		for region in regions:
			instances_region = []
			try:
				instances_region = instances[region]
			except:
				continue

			client = boto3.client('ec2', region)
			# start instances 
			response = client.start_instances(InstanceIds=instances_region)
			for instance in instances_region:
				log_data_csv += f"{region}, {instance}, started\n"
			log_data = log_data + "Started instances in region "  + region + ": " + arrayToString(instances_region) + "\n"
			print("Started instances in region "  + region + ": " + arrayToString(instances_region) + "\n")
			
		log_data = log_data + "Start command finished at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print("Start command finished at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

	elif command.lower() == "stop":
		log_data = log_data + "Stop command started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print("Stop command started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
		for region in regions:
			instances_region = []
			try:
				instances_region = instances[region]
			except:
				continue

			client = boto3.client('ec2', region)
			response = client.stop_instances(InstanceIds=instances_region)
			for instance in instances_region:
				log_data_csv += f"{region}, {instance}, stopped\n"
			log_data = log_data + "Stopped instances in region "  + region + ": " + arrayToString(instances_region) + "\n"
			print("Stopped instances in region "  + region + ": " + arrayToString(instances_region) + "\n")
			
		log_data = log_data + "Stop command finished at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print("Stop command finished at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")

	else:
		log_data = log_data + "Command " + command + " not mapped."
		print("Command " + command + " not mapped.")

	sendLogFileEmail(log_data, log_data_csv)
	#bucket = s3.Bucket(log_bucket)
	#bucket.put_object(Key=log_file, Body=log_data)
	#log_file_csv = log_file.replace(".log", ".csv")
	#bucket.put_object(Key=log_file_csv, Body=log_data_csv)
	return {"success": True, "message": "OK"}
 
 



def main():
	if len(sys.argv) == 2:
		file_name = sys.argv[1]
		json_file = json.loads(open(file_name, "rb").read())
		lambda_handler(json_file, None)
	else:
		parser = argparse.ArgumentParser()
		#parser.add_argument("file", type=str, help="File name of JSON file")
		parser.add_argument("-f", dest="file",  required=False, type=str, help="File name of JSON file")
		parser.add_argument("-s", dest="start",  required=False, type=str, help="Receive this parameter to start")
		parser.add_argument("-k", dest="stop",   required=False, type=str, help="Receive this parameter to stop")
		#parser.add_argument("-b", dest="bucket", required=False, type=str, help="Bucket name to store log")
		parser.add_argument("-u", dest="url",  required=False, type=str, help="URL of API Gateway")
		parser.add_argument("-p", dest="start2",  required=False, type=str, help="Receive this parameter to start")
		parser.add_argument("-q", dest="stop2",   required=False, type=str, help="Receive this parameter to stop")
		args = parser.parse_args()
		
		#If receive -u -p or -q
		if args.url is not None:
			url = args.url
			json_file = {
            	"instances": {
            		"us-east-1": [
						"i-0853b68fd170db975"
					],
            		"us-west-2": [
						"i-0893bf0d78af6d127"
					]
  				}
			}
			if args.start2 is not None:
				json_file["command"] = "start"
			elif args.stop2 is not None:
				json_file["command"] = "stop"
			
			response = requests.post(url, json=json_file)
			print(response.text)
		#If receive -f -s -or -k
		else:
			json_file = json.loads(open(args.file, "rb").read())
			if args.start is not None:
				json_file["command"] = "start"
			elif args.stop is not None:
				json_file["command"] = "stop"
			
			lambda_handler(json_file, None)
			#if args.bucket is None:
			#	print(f"Not received bucket name")
			#	return None
			#else:
			#	json_file["bucket"] = args.bucket

			

if __name__ == '__main__':
	main()
##python start-stop-ec2.py -s start -f nodes.json
##python start-stop-ec2.py -k start -f nodes.json

##python start-stop-ec2.py -p start -u 
##python start-stop-ec2.py -p stop -u 
