import boto3
import argparse
import json

parser = argparse.ArgumentParser(description='Arguments for managing ecs services')
action = parser.add_mutually_exclusive_group(required=True)
action.add_argument('-t', '--task', dest='taskConf',
                    help='task Config to pass for parsing.')
action.add_argument('-c', '--create', dest='createConf',
                    help='REQUIRED/EXCLUSIVE : Create a service from task definition')
action.add_argument('-u', '--update', dest='updateConf',
                    help='REQUIRED/EXCLUSIVE : Update a service')
action.add_argument('-d', '--delete', dest='deleteConf',
                    help='REQUIRED/EXCLUSIVE : Delete a service from specified cluster')


def registerTask(confFile):
    with open(confFile) as config:
        confParser = json.load(config)

    region = confParser['containers']['region']
    client = boto3.client('ecs', region_name=region)
    failedResponseCode = 503
    # setup parameter for task-def registration
    args = {}

    args['family'] = confParser['containers']['family']
    args['containerDefinitions'] = confParser['containers']['containerDefinitions']
    try:
        args['volumes'] = confParser['containers']['volumes']
    except:
        pass
    try:
        args['taskRoleArn'] = confParser['containers']['taskRoleArn']
    except:
        pass

    try:
        args['networkMode'] = confParser['containers']['networkMode']
    except:
        args['networkMode'] = 'bridge'

    try:
        args['placementConstraints'] = confParser['containers']['placementConstraints']
    except:
        pass
    try:
        args['requiresCompatibilities'] = confParser['containers']['requiresCompatibilities']
    except:
        pass
    try:
        args['cpu'] = confParser['containers']['cpu']
    except:
        pass
    try:
        args['memory'] = confParser['containers']['memory']
    except:
        pass

    # Register task-def
    try:
        print("Registerring/updating task def: {} ".format(confParser['containers']['family']))
        response = client.register_task_definition(**args)
        responseCode = response['ResponseMetadata']['HTTPStatusCode']
        if responseCode == 200:
            print("Task registered successfully...")
            print(responseCode)
        return responseCode
    except Exception as err:

        print(err)
        print("Service task creation or update failed")
        print("Response::: {} ".format(failedResponseCode))
        return failedResponseCode


def runTask(confFile):
    with open(confFile) as config:
        confParser = json.load(config)

    region = confParser['containers']['region']
    client = boto3.client('ecs', region_name=region)
    failedResponseCode = 503
    # setup parameter for task-def registration
    args = {}

    try:
        args['cluster'] = confParser['containers']['cluster']
    except:
        pass
    try:
        args['taskDefinition'] = confParser['containers']['taskDefinition']
    except:
        print("Need taskDefinition for runnnig task")
        return failedResponseCode
    try:
        args['overrides'] = confParser['containers']['overrides']
    except:
        pass
    try:
        args['count'] = confParser['containers']['count']
    except:
        pass
    try:
        args['startedBy'] = confParser['containers']['startedBy']
    except:
        pass
    try:
        args['group'] = confParser['containers']['group']
    except:
        pass
    try:
        args['placementConstraints'] = confParser['containers']['placementConstraints']
    except:
        pass
    try:
        args['placementStrategy'] = confParser['containers']['placementStrategy']
    except:
        pass
    try:
        args['launchType'] = confParser['containers']['launchType']
    except:
        pass
    try:
        args['platformVersion'] = confParser['containers']['platformVersion']
    except:
        pass
    try:
        args['networkConfiguration'] = confParser['containers']['networkConfiguration']
    except:
        print("Need networkConfiuration for running task")
        return failedResponseCode

    # Register task-def
    try:
        print("Running task def: {} ".format(confParser['containers']['taskDefinition']))
        response = client.run_task(**args)
        responseCode = response['ResponseMetadata']['HTTPStatusCode']
        if responseCode == 200:
            print("Running task successfully...")
            print(responseCode)
        return responseCode
    except Exception as err:

        print(err)
        print("Fail to run the task")
        print("Response::: {} ".format(failedResponseCode))
        return failedResponseCode


def deleteService(confFile):
    with open(confFile) as config:
        confParser = json.load(config)

    failedResponseCode = 503
    region = confParser['containers']['region']
    client = boto3.client('ecs', region_name=region)
    args = {}
    args['cluster'] = confParser['containers']['serviceDelete']['cluster']
    args['service'] = confParser['containers']['serviceDelete']['serviceName']
    try:
        args['force'] = confParser['containers']['serviceDelete']['force']
    except:
        force = ''

    try:

        print("Deleting service {} ".format(confParser['containers']['serviceDelete']['serviceName']))
        deleteResponse = client.delete_service(**args)
        responseCode = deleteResponse['ResponseMetadata']['HTTPStatusCode']

        if responseCode == 200:
            print("Response::: {} ".format(responseCode))
            return responseCode

        else:
            return responseCode

    except Exception as err:
        print(err)
        print("deleting service failed")
        print("Response::: {}".format(failedResponseCode))
        return failedResponseCode


def updateService(confFile):
    with open(confFile) as config:
        confParser = json.load(config)

    failedResponseCode = 503
    region = confParser['containers']['region']
    client = boto3.client('ecs', region_name=region)

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
            args['healthCheckGracePeriodSeconds'] = confParser['containers']['serviceUpdate'][
                'healthCheckGracePeriodSeconds']
        except:
            healthCheckGracePeriodSeconds = 123

        try:

            print("Updating service {}".format(confParser['containers']['serviceUpdate']['serviceName']))
            updateResponse = client.update_service(**args)

            responseCode = updateResponse['ResponseMetadata']['HTTPStatusCode']

            if responseCode == 200:
                print("Response::: {}".format(responseCode))
                return responseCode

            else:
                return responseCode

        except Exception as err:
            print(err)
            print("Service update failed")
            print("Response::: {}".format(failedResponseCode))
            return failedResponseCode


def createService(confFile):
    with open(confFile) as config:
        confParser = json.load(config)

    failedResponseCode = 503
    region = confParser['containers']['region']
    client = boto3.client('ecs', region_name=region)

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
            args['healthCheckGracePeriodSeconds'] = confParser['containers']['serviceCreate'][
                'healthCheckGracePeriodSeconds']
        except:
            healthCheckGracePeriodSeconds = 123
        try:
            args['schedulingStrategy'] = confParser['containers']['serviceCreate']['schedulingStrategy']
        except:
            schedulingStrategy = ''

        try:
            print("Creating service {}".format(confParser['containers']['serviceCreate']['serviceName']))
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

    if args.taskConf is not None:
        print("task registration....\n")
        if registerTask(args.taskConf) == 200:
            print("task running...\n")

    elif args.createConf is not None:
        print("create request recieved........\n")
        createService(args.createConf)

    elif args.updateConf:
        print("update request recieved........\n")
        updateService(args.updateConf)

    elif args.deleteConf:
        print("Delete request recieved........\n")
        confirmation = input('*****CAUTION: Deleting service******.\nEnter "yes" to continue: ')
        if confirmation == 'yes':
            deleteService(args.deleteConf)
        else:
            print("exiting...")
