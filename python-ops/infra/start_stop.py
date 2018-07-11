import boto3
import datetime
import sys
import json
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart



log_file = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M") + "-start_stop.log"
regions = ['us-east-1', 'us-east-2', 'us-west-1', 'us-west-2', 'ca-central-1', 'eu-central-1', 'eu-west-1', 'eu-west-2', 'eu-west-3', 'ap-northeast-1', 'ap-northeast-2', 'ap-southeast-1', 'ap-southeast-2', 'ap-south-1', 'sa-east-1']

def sendLogFileEmail(log_data):
	message = MIMEMultipart()
	message['Subject'] = log_file
	message['From'] = 'chakraborty.rock@gmail.com'
	message['To'] = 'sudipta1436@gmail.com'

	# what a recipient sees if they don't use an email reader
	message.preamble = 'Multipart message.\n'

	# the message body
	message.attach(MIMEText('status of service'))	
	part = MIMEApplication(log_data)
	part.add_header('Content-Disposition', 'attachment; filename="%s"' % log_file)
	message.attach(part)
	client = boto3.client('ses')
	response = client.send_raw_email (Source='chakraborty.rock@gmail.com',Destinations=['sudipta1436@gmail.com'],RawMessage={'Data': message.as_string()})
	#print "E-mail sent: " + str(response)

def arrayToString(x):
	if len(x) == 1:
		return x[0]
	else:
		return x[0] + ", " + arrayToString(x[1:])

def lambda_handler(event, context):
	command = event["command"]
	log_bucket = event["log-bucket"]
	instances = event["instances"]

	s3 = boto3.resource('s3')

	log_data = ""

	if command.lower() == "start":
		log_data = log_data + "Start command started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print "Start command started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"

		for region in regions:
			instances_region = []
			try:
				instances_region = instances[region]
			except:
				continue

			client = boto3.client('ec2', region)
			response = client.start_instances(InstanceIds=instances_region)
			log_data = log_data + "Started instances in region "  + region + ": " + arrayToString(instances_region) + "\n"
			print "Started instances in region "  + region + ": " + arrayToString(instances_region) + "\n"
			
		log_data = log_data + "Start command finished at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print "Start command finished at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		
	elif command.lower() == "stop":
		log_data = log_data + "Stop command started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print "Stop command started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		for region in regions:
			instances_region = []
			try:
				instances_region = instances[region]
			except:
				continue

			client = boto3.client('ec2', region)
			response = client.stop_instances(InstanceIds=instances_region)
			log_data = log_data + "Stopped instances in region "  + region + ": " + arrayToString(instances_region) + "\n"
			print "Stopped instances in region "  + region + ": " + arrayToString(instances_region) + "\n"
			
		log_data = log_data + "Stop command finished at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print "Stop command finished at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"

	elif command.lower() == "terminate":
		log_data = log_data + "Terminate command started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n"
		print "Terminate command started at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + "\n"

		for region in regions:
			instances_region = []
			try:
				instances_region = instances[region]
			except:
				continue

			client = boto3.client('ec2', region)
			response = client.terminate_instances(InstanceIds=instances_region)
			log_data = log_data + "Terminated instances in region " + region + ": " + arrayToString(instances_region) + "\n"
			
			print "Terminated instances in region " + region + ": " +  arrayToString(instances_region) + "\n"
		
		log_data = log_data + "Terminate command finished at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"
		print "Terminate command finished at " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n"

	else:
		log_data = log_data + "Command " + command + " not mapped."
		print "Command " + command + " not mapped."

	sendLogFileEmail(log_data)
	s3.Bucket(log_bucket).put_object(Key=log_file, Body=log_data)

if __name__=="__main__":
	file_name = sys.argv[1]
	json_file = json.loads(open(file_name, "rb").read())
	lambda_handler(json_file, None)