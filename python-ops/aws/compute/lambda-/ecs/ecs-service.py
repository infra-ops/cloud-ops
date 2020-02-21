import boto3
import argparse
import json

parser = argparse.ArgumentParser(description='Arguments for managing ecs services')

action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('-t', '--task', dest='taskConf',
                    help='task Config to pass for parsing.')
action.add_argument('-c', '--create', dest='createConf',
                    help='REQUIRED/EXCLUSIVE : Create a service from task definition')

common_params = parser.add_argument_group('common')

parser.add_argument('-r', '--region', dest='region', default='us-east-1',
                    help='AWS Region')

def registerTask(confFile, region):
    with open(confFile) as config:
        confParser = json.load(config)
    client = boto3.client('ecs', region_name=region)
    failedResponseCode = 503
    # setup parameter for task-def registration
    args = {}

    args['family'] = confParser['family']
    args['containerDefinitions'] = confParser['containerDefinitions']
    try:
        args['volumes'] = confParser['volumes']
    except:
        pass
    try:
        args['taskRoleArn'] = confParser['taskRoleArn']
    except:
        pass

    try:
        args['networkMode'] = confParser['networkMode']
    except:
        args['networkMode'] = 'bridge'

    try:
        args['placementConstraints'] = confParser['placementConstraints']
    except:
        pass
    try:
        args['requiresCompatibilities'] = confParser['requiresCompatibilities']
    except:
        pass
    try:
        args['cpu'] = confParser['cpu']
    except:
        pass
    try:
        args['memory'] = confParser['memory']
    except:
        pass

    # Register task-def
    try:
        print("Registerring/updating task def: {} ".format(confParser['family']))
        response = client.register_task_definition(**args)
        #print (response)
        responseCode = response['ResponseMetadata']['HTTPStatusCode']
        if responseCode == 200:
            print("Task registered successfully. Please use the following task definition to create or update service!")
            print(response['taskDefinition']['taskDefinitionArn'].split('/')[-1])
            print(responseCode)
        return responseCode
    except Exception as err:

        print(err)
        print("Service task creation or update failed")
        print("Response::: {} ".format(failedResponseCode))
        return failedResponseCode

def createService(confFile, region):
    with open(confFile) as config:
        confParser = json.load(config)

    failedResponseCode = 503
    client = boto3.client('ecs', region_name=region)

    regResponse = 200
    args = {}
    if regResponse == 200:

        args['cluster'] = confParser['cluster']
        args['serviceName'] = confParser['serviceName']
        args['taskDefinition'] = confParser['taskDefinition']
        args['desiredCount'] = confParser['desiredCount']
        args['clientToken'] = confParser['clientToken']
        try:
            args['launchType'] = confParser['lauchType']
        except:
            launchType = ''
        try:
            args['platformVersion'] = confParser['platformVersion']
        except:
            platformVersion = ''
        try:
            args['role'] = confParser['role']
        except:
            role = ''
        try:
            args['deploymentConfiguration'] = confParser['deploymentConfiguration']
        except:
            deploymentConfiguration = []
        try:
            args['loadBalancers'] = confParser['loadBalancers']
        except:
            loadBalancers = []

        try:
            args['placementConstraints'] = confParser['placementConstraints']
        except:
            placementConstraints = []
        try:
            args['placementStrategy'] = confParser['placementStrategy']
        except:
            placementStrategy = []
        try:
            args['networkConfiguration'] = confParser['networkConfiguration']
        except:
            networkConfig = []
        try:
            args['serviceRegistries'] = confParser['serviceRegistries']
        except:
            serviceRegistries = []
        try:
            args['healthCheckGracePeriodSeconds'] = confParser[
                'healthCheckGracePeriodSeconds']
        except:
            healthCheckGracePeriodSeconds = 123
        try:
            args['schedulingStrategy'] = confParser['schedulingStrategy']
        except:
            schedulingStrategy = ''

        try:
            print("Creating service {}".format(confParser['serviceName']))
            createResponse = client.create_service(**args)
            responseCode = createResponse['ResponseMetadata']['HTTPStatusCode']

            if responseCode == 200:
                print("Response::: {}".format(responseCode))
                return responseCode

            else:
                return responseCode

        except Exception as err:
            print(err)
            print("Service creation failed")
            print("Response::: {}".format(failedResponseCode))
            return failedResponseCode


if __name__ == '__main__':
    # Call the parser to get the values
    args = parser.parse_args()
    print (args)

    if args.taskConf is not None:
        print("task registration....\n")
        if registerTask(args.taskConf, args.region) == 200:
            print("task definition created. Please proceed with service creation/updation!!!\n")

    elif args.createConf is not None:
        print("service create request recieved........\n")
        createService(args.createConf, args.region)
        print ("Service created successfully!!")
