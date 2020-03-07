from builtins import ValueError, Exception, str
import boto3
import json
import logging
import os
import sys
'''
Initialziation block for intializing logger and constants.
'''
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if 'LOG_LEVEL' in os.environ:
    if os.environ['LOG_LEVEL'] == 'DEBUG':
        logger.setLevel(logging.DEBUG)
    if os.environ['LOG_LEVEL'] == 'INFO':
        logger.setLevel(logging.INFO)
    if os.environ['LOG_LEVEL'] == 'WARNING':
        logger.setLevel(logging.WARNING)
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Methods': 'POST,OPTIONS',
    'Access-Control-Allow-Credentials': True,
    'Content-Type': 'application/json'
}
def lambda_handler(event, context):
    logger.debug("Received event: %s", json.dumps(event))
    try:
        payload = json.loads(event['body'])
        region = payload['region']
        service_name = payload['service']
        cluster = payload['cluster']
        image = payload['image']
        ecs_client = boto3.client('ecs', region)
        resp = ecs_client.describe_services(
            cluster=cluster,
            services=[service_name])
        if len(resp['services']) == 0:
            raise Exception("Unable to find Service in the Cluster. Please check!")
        service_config = resp['services'][0]
        logger.info("Describe Service resp: {} ".format(str(service_config)))
        task_def = service_config['taskDefinition'].split("/")[-1]
        logger.info("Task def is : {} ".format(task_def))
        task_def_config = ecs_client.describe_task_definition(taskDefinition=task_def)
        logger.info("Task def config : {} ".format(str(task_def_config)))
        new_task_def_config = task_def_config['taskDefinition']
        new_task_def_config.pop("taskDefinitionArn")
        new_task_def_config['requiresCompatibilities'] = new_task_def_config['compatibilities']
        new_task_def_config['containerDefinitions'][0]['image'] = image
        new_task_def_config.pop("revision")
        new_task_def_config.pop("status")
        new_task_def_config.pop("compatibilities")
        new_task_def_config.pop("requiresAttributes")
        logger.info("New taskdef attributes are: {} ".format(json.dumps(new_task_def_config)))
        update_task_def_resp = ecs_client.register_task_definition(**new_task_def_config)
        logger.info(update_task_def_resp)
        new_task_def_revision = update_task_def_resp['taskDefinition']['taskDefinitionArn'].split('/')[-1]
        if 'desiredCount' in payload:
            update_service_response = ecs_client.update_service(
                cluster=cluster,
                service=service_name,
                desiredCount=payload['desiredCount'],
                taskDefinition=new_task_def_revision)
        else:
            update_service_response = ecs_client.update_service(
                cluster=cluster,
                service=service_name,
                taskDefinition=new_task_def_revision)
        return {
            'statusCode': 200,
            'headers': headers,
            'body': json.dumps({"taskDef":str(update_service_response)})
        }
    except ValueError as ve:
        logger.error(str(ve))
        return {
            'statusCode': 400,
            'headers': headers,
            'body': json.dumps({"errorMessage": str(ve)})
        }
    except Exception as ex:
        logger.error(str(ex))
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({"errorMessage": str(ex)})
        }
def get_mandatory_evar(evar_name):
    if not evar_name in os.environ:
        raise ValueError("Missing environment variable: {}".format(evar_name))
    return os.environ[evar_name]
def get_mandatory_event_attr(event, attr):
    if not attr in event:
        raise ValueError("Missing event attribute: {}".format(attr))
    return event[attr]
if __name__=='__main__':
    file = sys.argv[1]
    with open(file) as input:
        body = json.load(input)
    print (lambda_handler({"body":json.dumps(body)},""))
