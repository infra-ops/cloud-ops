#!/bin/bash
e=`aws ecs list-task-definitions | grep -i tomcat | cut -d "/" -f2 | cut -d ":" -f1`
s=`aws ecs create-service --cli-input-json file://tomcat-svc-cli.json`
t=`aws ecs register-task-definition --cli-input-json file://tomcat-task-cli.json`
#echo $e
    if [[ -z "$e" ]] ;then
        echo "create ecs service:$t"
   #      ${e}
        #aws ecs create-service --cli-input-json file://tomcat-svc-cli.json
    else
        echo "create ecs task:$s"
    #     ${t}
       #aws ecs register-task-definition --cli-input-json file://tomcat-task-cli.json
    fi
