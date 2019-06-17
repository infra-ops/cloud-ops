#!/bin/bash

echo $WORKSPACE
dt=`date "+%Y-%m-%d-%H-%M"`


war1=`ls -lrt /var/lib/jenkins/workspace/war-deploy-1/target/ | grep -i .war | awk '{print $NF}'`
#war2=`curl --silent -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText" | grep -i Building  | awk -F "/"  '{print $NF}' | awk 'END { print }'`
echo $war1

aws s3 cp /var/lib/jenkins/workspace/war-deploy-1/target/$war1 s3://hello-artifactory/$dt/$war1 --acl public-read-write


curl -i \
-u admin:password \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data '{"extra_vars":{"ear_ver": "$(war1)"}}' "http://localhost/api/v2/job_templates/21/launch/"



war1=`ls -lrt /var/lib/jenkins/workspace/war-deploy-1/target/ | grep -i .war | awk -F "/" '{print $NF}'`
echo $war1
curl -i \
-u admin:password \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data '{"extra_vars":{"ear_ver": "$\{war1\}"}}' "http://localhost/api/v2/job_templates/21/launch/"




war1=`ls -lrt /var/lib/jenkins/workspace/war-deploy-1/target/ | grep -i .war | awk -F "/" '{print $NF}'`
echo $war1
curl -i \
-u admin:password \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data '{"extra_vars":{"ear_ver": "${war1}"}}' "http://localhost/api/v2/job_templates/21/launch/"




