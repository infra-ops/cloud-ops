import boto3
import json
"""

from defaults import (
    get_default_task,
    get_default_service
)

"""
def load_json(file):
    string_input = open(file, "r").read()
    return json.loads(string_input)

def update_task_definition_image(taskDefinition, image, region):
    client = boto3.client('ecs', region)
    response = client.describe_task_definition(
        taskDefinition=taskDefinition
    )
    taskDefinitionJSON = response["taskDefinition"]
    del taskDefinitionJSON["taskDefinitionArn"]
    for containerDefinition in taskDefinitionJSON.get("containerDefinitions", []):
        containerDefinition["image"] = image
    
    response = create_task(taskDefinitionJSON, region)
    return response["taskDefinition"]["taskDefinitionArn"]

def get_service_task_definition(cluster, service, region):
    client = boto3.client('ecs', region)
    response = client.describe_services(
        cluster=cluster,
        services=[service]
    )
    return response["services"][0]["taskDefinition"]

def delete_service(service, cluster, region):
    client = boto3.client('ecs', region)
    response = client.delete_service(
        cluster=cluster,
        service=service,
        force=True
    )
    return response

def deregister_task_definition(taskDefinition, region):
    client = boto3.client('ecs', region)

    response = client.deregister_task_definition(
        taskDefinition=taskDefinition
    )

    return response

def update_service(json, region):
    client = boto3.client('ecs', json.get("region", region))


    service      = json.get("service")
    cluster      = json.get("cluster")
    image        = json.get("image")
    desiredCount = json.get("desiredCount")

    task_definition         = get_service_task_definition(cluster, service, json.get("region", region))
    new_task_definition_arn = update_task_definition_image(task_definition, image, json.get("region", region))

    response = client.update_service(
        cluster=cluster,
        service=service,
        desiredCount=desiredCount,
        taskDefinition=new_task_definition_arn
    )

    return response

def create_service(json, region):
    client = boto3.client('ecs', json.get("region", region))
    
    cluster        = json.get("cluster")
    serviceName    = json.get("serviceName")
    taskDefinition = json.get("taskDefinition")
    desiredCount   = json.get("desiredCount")
    clientToken    = json.get("clientToken")
    launchType     = json.get("launchType")
    loadBalancers  = json.get("loadBalancers")
    deployConfig   = json.get("deploymentConfiguration", {"maximumPercent": 200, "minimumHealthyPercent": 50})

    response = client.create_service(
        cluster=cluster,
        serviceName=serviceName,
        taskDefinition=taskDefinition,
        loadBalancers=loadBalancers,
        desiredCount=desiredCount,
        launchType=launchType,
        clientToken=clientToken,
        deploymentConfiguration=deployConfig
    )
    return response

def stop_task(cluster, task, region):
    client = boto3.client('ecs', region)

    response = client.stop_task(
        cluster=cluster,
        task=task
    )

    return response

def create_task(json, region):
    client = boto3.client('ecs', json.get("region", region))

    memory       = json.get("memory")
    family       = json.get("family")
    networkMode  = json.get("networkMode")
    cpu          = json.get("cpu")
    containerDef = json.get("containerDefinitions")
    requiresComp = json.get("requiresCompatibilities")
    
    response = client.register_task_definition(
        family=family,
        cpu=cpu,
        memory=memory,
        networkMode=networkMode,
        containerDefinitions=containerDef,
        requiresCompatibilities=requiresComp
    )

    return response

def lambda_handler(event, context):
    action = event.get("action")

    try:
        response = ""
        if action == "create":
            cluster = event.get("cluster", None)
            if cluster is not None:
                response = create_service(
                    event, 
                    event.get("region", "us-east-1")
                )
                response = f"Created {response['service']['serviceArn']}"
            else:
                json = get_default_task()
                json["containerDefinitions"][0]["image"] = event.get("image")
                json["containerDefinitions"][0]["name"]  = event.get("name")
                json["family"]                           = event.get("name")
                response = create_task(
                    json,
                    event.get("region", "us-east-1")
                )
        elif action == "update":
            response = update_service(
                event, 
                event.get("region", "us-east-1")
            )
            response = f"Updated {response['service']['serviceArn']}"
        elif action == "taskderegester":
            taskDefinition = event.get("name")
            response = deregister_task_definition(
                taskDefinition,
                event.get("region", "us-east-1")
            )
        elif action == "svcdelete":
            service = event.get("service")
            cluster = event.get("cluster")
            response = delete_service(
                service,
                cluster,
                event.get("region", "us-east-1")
            )
            response = f"Deleted {response['service']['serviceArn']}"
        elif action == "taskstop":
            cluster = event.get("cluster")
            task    = event.get("task")
            response = stop_task(
                cluster,
                task,
                event.get("region", "us-east-1")
            )
            response = f"Stopped task {response['task']['taskArn']}"
        else:
            return {
                "success": False,
                "message": "Received action is not of type create, update, deregister or delete"
            }
        return {
            "success": True,
            "message": response
        }
    except Exception as exception:
        return {
            "success": False,
            "message": str(exception)
        }
        
    if event.get("type") == "task":
        return create_task(event, event.get("region", "us-east-1"))
    else:
        return create_task(event, event.get("region", "us-east-1"))

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Arguments for managing ECS Services')
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('-t', dest='task', help='Create Task configuration to pass for parsing.')
    action.add_argument('-s', dest='service', help='Create Service configuration to pass for parsing')
    action.add_argument('-u', dest='update', help='Update Service configuration to pass for parsing')
    action.add_argument('-d', dest='deregister', help='Deregister Task configuration to pass for parsing')
    action.add_argument('-k', dest='kill', help='Delete Service configuration to pass for parsing')
    parser.add_argument('-e', dest='cluster', help='The name of the ECS Cluster')
    parser.add_argument('-a', dest='stop', help='Stop task')
    parser.add_argument('-tid', dest='taskid', help='Stop task')
    parser.add_argument('-r', dest='region', default='us-east-1', help='AWS Region')


    args = parser.parse_args()

    if args.task is not None:
        json = load_json(args.task)
        response = create_task(json , args.region)
        print(response)
    elif args.service is not None:
        json = load_json(args.service)
        response = create_service(json, args.region)
        print(response)
    elif args.update is not None:
        json = load_json(args.update)
        response = update_service(json, args.region)
        print(response)
    elif args.deregister is not None:
        response = deregister_task_definition(args.deregister, args.region)
        print(response)
    elif args.kill is not None and args.cluster is not None:
        response = delete_service(args.kill, args.cluster, args.region)
        print(response)
    elif args.stop is not None or args.taskid is not None:
        response = stop_task(args.cluster, args.taskid, args.region)
        print(response)
    else:
        print("Kindly parse correct key")

if __name__ == "__main__":
    main()

#present
#python ecs-service-v.0.9.py  -t tom-task.json # to create task from tty
#python ecs-service-v.0.9.py  -s tom-svc.json # to create svc from tty
#python ecs-service-v.0.9.py  -u tom-svc.json # to update svc from tty
#python ecs-service-v.0.9.py  -e connector-clus -k test-service-5 # to delete service from tty
#python ecs-service-v.0.9.py  -a taskstop -e connector-clus -tid 8358790f-6d48-4a4d-bbf2-384cf581490b # to stop service from tty
#python ecs-service-v.0.9.py  -e connector-clus -d tomcat-23:3 # to deregister task revision from  tty

#New
#python ecs-service-v.0.9.py  -a taskcreate -t tom-task.json # to create task from tty
#python ecs-service-v.0.9.py  -a svccreate  -s tom-svc.json # to create svc from tty
#python ecs-service-v.0.9.py  -a svcupdate -u tom-svc.json # to update svc from tty
#python ecs-service-v.0.9.py  -a svcstop   -e connector-clus -k test-service-5 # to delete service from tty
#python ecs-service-v.0.9.py  -a taskstop -e connector-clus -tid 8358790f-6d48-4a4d-bbf2-384cf581490b # to stop service from tty
#python ecs-service-v.0.9.py  -a deregister -e connector-clus -d tomcat-23:3 # to deregister task revision from  tty