

def get_default_task():
    return {
        "memory": "256",
        "family": "tomcat-webserver-2",
        "networkMode": "bridge",
        "cpu": "1024",
        "containerDefinitions": [
            {
                "logConfiguration": {
                    "logDriver": "awslogs",
                    "options": {
                        "awslogs-group": "/ecs/tomcat-container-logs",
                        "awslogs-region": "us-east-1",
                        "awslogs-stream-prefix": "ecs"
                    }
                },
                "portMappings": [
                    {
                        "hostPort": 9090,
                        "protocol": "tcp",
                        "containerPort": 9090
                    }
                ],
                "cpu": 1024,
                "memory": 256,
                "image": "758637906269.dkr.ecr.us-east-1.amazonaws.com/connector-dev:22",
                "essential": True,
                "name": "tomcat-webserver-2"
            }
        ],
        "requiresCompatibilities": [
            "EC2"
        ]
    }

def get_default_service():
    return {
        "cluster": "connector-clus",
        "serviceName": "test-service-5",
        "taskDefinition": "tomcat-webserver-2:32",
        "desiredCount": 1,
        "clientToken": "test-service-1",
        "launchType": "EC2",
        "loadBalancers": [
            {
                "targetGroupArn": "arn:aws:elasticloadbalancing:us-east-1:758637906269:targetgroup/tomcat-demo-tg/510d919f193f067e",
                "containerName": "tomcat-webserver-2",
                "containerPort": 9090
            }
        ],
        "deploymentConfiguration": {
            "maximumPercent": 200,
            "minimumHealthyPercent": 50
        }
    }
