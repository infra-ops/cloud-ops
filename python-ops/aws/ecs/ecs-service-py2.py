import boto3
import argparse
import yaml
import json


parser=argparse.ArgumentParser(description='Arguments for managing ecs services')
parser.add_argument('-c',action='store',dest='serviceConfFile',default=None,help='service Config to pass for parsing.')
parser.add_argument('-t',action='store',dest='taskConfFile',default=None,help='task Config to pass for parsing.')
action=parser.add_mutually_exclusive_group(required=False)
action.add_argument('--create',action='store_true',help='REQUIRED/EXCLUSIVE : Create a service from task definition')
action.add_argument('--update',action='store_true',help='REQUIRED/EXCLUSIVE : Update a service')
action.add_argument('--delete',action='store_true',help='REQUIRED/EXCLUSIVE : Delete a service from specified cluster')


def registerTask(confFile):
	with open(confFile) as config:
		confParser =  json.load(config)

	region = confParser['containers']['region']
	client = boto3.client('ecs',region_name=region)
	failedResponseCode = 503
	# setup parameter for task-def registration
	args = {}

	args['family']=confParser['containers']['family']
	args['containerDefinitions']=confParser['containers']['containerDefinitions']
	try:
		args['volumes']=confParser['containers']['volumes']
	except:
		pass
	try:
		args['taskRoleArn']=confParser['containers']['taskRoleArn']
	except:
		pass

	try:
		args['networkMode'] = confParser['containers']['networkMode']
	except:
		args['networkMode'] = 'bridge'

	try:
		args['placementConstraints']= confParser['containers']['placementConstraints']
	except:
		pass
	try:
		args['requiresCompatibilities'] = confParser['containers']['requiresCompatibilities']
	except:
		pass
	try:
		args['cpu']= confParser['containers']['cpu']
	except:
		pass
	try:
		args['memory'] = confParser['containers']['memory']
	except:
		pass
    
	# Register task-def
	try:
		print "Registerring/updating task def: %s " %(confParser['containers']['family'])
		response = client.register_task_definition(**args)
		responseCode=response['ResponseMetadata']['HTTPStatusCode']
		if responseCode == 200:
			print "Task registered successfully..."
			print responseCode
		return responseCode
	except Exception,err:

		print err
		print "Service task creation or update failed"
		print "Response::: %s " %(failedResponseCode)
		return failedResponseCode
def runTask(confFile):
	with open(confFile) as config:
		confParser =  json.load(config)

	region = confParser['containers']['region']
	client = boto3.client('ecs',region_name=region)
	failedResponseCode = 503
	# setup parameter for task-def registration
	args = {}

	try:
		args['cluster']=confParser['containers']['cluster']
	except:
		pass	
	try:
		args['taskDefinition']=confParser['containers']['taskDefinition']
	except:
		print "Need taskDefinition for runnnig task"
		return failedResponseCode
	try:
		args['overrides']=confParser['containers']['overrides']
	except:
		pass
	try:
		args['count']=confParser['containers']['count']
	except:
		pass
	try:
		args['startedBy'] = confParser['containers']['startedBy']
	except:
		pass
	try:
		args['group']= confParser['containers']['group']
	except:
		pass
	try:
		args['placementConstraints'] = confParser['containers']['placementConstraints']
	except:
		pass
	try:
		args['placementStrategy']= confParser['containers']['placementStrategy']
	except:
		pass
	try:
		args['launchType'] = confParser['containers']['launchType']
	except:
		pass
	try:
		args['platformVersion']= confParser['containers']['platformVersion']
	except:
		pass
	try:
		args['networkConfiguration'] = confParser['containers']['networkConfiguration']
	except:
		print "Need networkConfiuration for running task"
		return failedResponseCode
    
	# Register task-def
	try:
		print "Running task def: %s " %(confParser['containers']['taskDefinition'])
		response = client.run_task(**args)
		responseCode=response['ResponseMetadata']['HTTPStatusCode']
		if responseCode == 200:
			print "Running task successfully..."
			print responseCode
		return responseCode
	except Exception, err:

		print err
		print "Fail to run the task"
		print "Response::: %s " %(failedResponseCode)
		return failedResponseCode

def deleteService(confFile):
	with open(confFile) as config:
		confParser =  json.load(config)

	failedResponseCode = 503
	region = confParser['containers']['region']
	client = boto3.client('ecs',region_name=region)
	args = {}
	args['cluster'] = confParser['containers']['serviceDelete']['cluster']
	args['service'] = confParser['containers']['serviceDelete']['serviceName']
	try:
		args['force'] = confParser['containers']['serviceDelete']['force']
	except:
		force = ''
	
	try:

		print "Deleting service %s " %(confParser['containers']['serviceDelete']['serviceName'])
		# If task def was registerred then create service 
		# deleteResponse = client.delete_service(cluster=clusterName,
		# 									   serviceName=serviceName,
		# 									   force=force)
		deleteResponse = client.delete_service(**args)
		responseCode = deleteResponse['ResponseMetadata']['HTTPStatusCode']  

		if responseCode == 200: 
			print "Response::: %s " %(responseCode)
			return responseCode

		else: 
			return responseCode

	except Exception,err:
		print err
		print "deleting service failed"
		print "Response::: %s" %(failedResponseCode)
		return failedResponseCode


def updateService(confFile):
	with open(confFile) as config:
		confParser =  json.load(config)

	failedResponseCode = 503
	region = confParser['containers']['region']
	client = boto3.client('ecs',region_name=region)

	regResponse = 200

	if regResponse == 200:   
		args = {}
		args['cluster'] = confParser['containers']['serviceUpdate']['cluster']
		args['service'] = confParser['containers']['serviceUpdate']['serviceName']
		args['taskDefinition'] = confParser['containers']['serviceUpdate']['taskDefinition']
		args['desiredCount'] = confParser['containers']['serviceUpdate']['desiredCount']

		try:
			args['deploymentConfiguration'] = confParser['containers']['serviceUpdate']['deploymentConfiguration']
		except:
			deploymentConfiguration = []
		try:
			args['networkConfiguration'] = confParser['containers']['serviceUpdate']['networkConfiguration']
		except:
			networkConfiguration = []
		try:
			args['platformVersion'] = confParser['containers']['serviceUpdate']['platformVersion']
		except:
			platformVersion = ''
		try:
			args['forceNewDeployment'] = confParser['containers']['serviceUpdate']['forceNewDeployment']
		except:
			forceNewDeployment = ''
		try:
			args['healthCheckGracePeriodSeconds'] = confParser['containers']['serviceUpdate']['healthCheckGracePeriodSeconds']
		except:
			healthCheckGracePeriodSeconds = 123

		try:

			print "Updating service %s" %(confParser['containers']['serviceUpdate']['serviceName'])
			# If task def was registerred then create service 
			# updateResponse = client.update_service(cluster=clusterName,
			# 									    service=serviceName,
			# 									    desiredCount=desiredCount,
			# 									    taskDefinition=taskDefinition,
			# 									    deploymentConfiguration=deploymentConfiguration,
			# 									    networkConfiguration=networkConfiguration,
			# 									    platformVersion=platformVersion,
			# 									    forceNewDeployment=forceNewDeployment,
			# 									    healthCheckGracePeriodSeconds=healthCheckGracePeriodSeconds)
			updateResponse = client.update_service(**args)

			responseCode = updateResponse['ResponseMetadata']['HTTPStatusCode']  

			if responseCode == 200: 
				print "Response::: %s" %(responseCode)
				return responseCode

			else: 
				return responseCode

		except Exception,err:
			print err
			print "Service update failed"
			print "Response::: %s" %(failedResponseCode)
			return failedResponseCode

def createService(confFile):
	with open(confFile) as config:
		confParser =  json.load(config)

	failedResponseCode = 503
	region = confParser['containers']['region']
	client = boto3.client('ecs',region_name=region)

	regResponse = 200
	args = {}
	if regResponse == 200:   

		args['cluster'] = confParser['containers']['serviceCreate']['cluster']
		args['serviceName'] = confParser['containers']['serviceCreate']['serviceName']
		args['taskDefinition'] = confParser['containers']['serviceCreate']['taskDefinition']
		args['desiredCount'] = confParser['containers']['serviceCreate']['desiredCount']
		args['clientToken'] = confParser['containers']['serviceCreate']['clientToken']
		try:
			args['launchType'] = confParser['containers']['serviceCreate']['lauchType']
		except:
			launchType = ''
		try:
			args['platformVersion'] = confParser['containers']['serviceCreate']['platformVersion']
		except:
			platformVersion = ''
		try:
			args['role'] = confParser['containers']['serviceCreate']['role']
		except:
			role = ''
		try:
			args['deploymentConfiguration'] = confParser['containers']['serviceCreate']['deploymentConfiguration']
		except:
			deploymentConfiguration = []
		try:
			args['loadBalancers'] = confParser['containers']['serviceCreate']['loadBalancers']
		except:
			loadBalancers = []

		try:
			args['placementConstraints'] = confParser['containers']['serviceCreate']['placementConstraints']
		except:
			placementConstraints = []
		try:
			args['placementStrategy'] = confParser['containers']['serviceCreate']['placementStrategy']
		except:
			placementStrategy = []
		try:
			args['networkConfiguration'] = confParser['containers']['serviceCreate']['networkConfiguration']
		except:
			networkConfig = []
		try:
			args['serviceRegistries'] = confParser['containers']['serviceCreate']['serviceRegistries']
		except:
			serviceRegistries = []
		try:
			args['healthCheckGracePeriodSeconds'] = confParser['containers']['serviceCreate']['healthCheckGracePeriodSeconds']
		except:
			healthCheckGracePeriodSeconds = 123
		try:
			args['schedulingStrategy'] = confParser['containers']['serviceCreate']['schedulingStrategy']
		except:
			schedulingStrategy = ''

		try:
			print "Creating service %s" %(confParser['containers']['serviceCreate']['serviceName'])
			# If task def was registerred then create service 
			# createResponse = client.create_service(cluster=clusterName,
			# 									   serviceName=serviceName,
			# 									   taskDefinition=taskDefinition,
			# 									   loadBalancers=loadBalancers,
			# 									   serviceRegistries=serviceRegistries,
			# 									   desiredCount=desiredCount,
			# 									   clientToken=clientToken,
			# 									   launchType=launchType,
			# 									   platformVersion=platformVersion,
			# 									   role=role,
			# 									   deploymentConfiguration=deploymentConfiguration,
			# 									   placementConstraints=placementConstraints,
			# 									   placementStrategy=placementStrategy,
			# 									   networkConfiguration=networkConfig,
			# 									   healthCheckGracePeriodSeconds=healthCheckGracePeriodSeconds,
			# 									   schedulingStrategy=schedulingStrategy
			# 									   )
			createResponse = client.create_service(**args)
			responseCode = createResponse['ResponseMetadata']['HTTPStatusCode']  

			if responseCode == 200: 
				print "Response::: %s" %(responseCode)
				return responseCode

			else: 
				return responseCode

		except Exception,err:
			print err
			print "Service creation failed"
			print "Response::: %s" %(failedResponseCode)
			return failedResponseCode

if __name__ == '__main__':
# Call the parser to get the values
	args = parser.parse_args()

	serviceConfFile = args.serviceConfFile
	taskConfFile = args.taskConfFile

	if args.create:
		print "create request recieved........\n"
		createService(serviceConfFile)

	elif args.update:
		print "update request recieved........\n"
		updateService(serviceConfFile)

	elif args.delete:
		print "Delete request recieved........\n"
		confirmation=input('*****CAUTION: Deleting service******.\nEnter "yes" to continue: ')
		if confirmation == 'yes':
			deleteService(serviceConfFile)
		else:
			print "exiting..." 

	else:
		print "task registration....\n" 
		if(registerTask(taskConfFile)==200):
			print "task running...\n"
			#runTask(taskConfFile)



	
	
