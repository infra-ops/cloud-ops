#data=$(curl --silent -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText" | grep -io "maven.*war$")
#echo $data
#data=$(curl --silent -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText" | sed 's/\(.*target\/\)\([A-Za-z].*war$\)/\2/')
#echo $data
#data=$(curl --silent -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText" | sed 's/\(.*target\/\)\([A-Za-z].*war$\)/\2/')
#echo $data
#data=$(echo "Building war: /var/lib/jenkins/workspace/war-deploy-1/target/mavenproject1-1.0-SNAPSHOT.war" | sed 's/\(.*target\/\)\(.*war$\)/\2/')

#data=$(curl --silent -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText" | sed 's/\(.*target\/\)\(.*war$\)/\2/')
#echo $data



#data=`curl --silent -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText" | grep -i Building  | awk '{print $4;}' | sed -n '3p' | cut -d "/" -f8`
#echo $data

#1.
#data=`curl --silent -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText" | grep -i Building  | awk -F "/"  '{print $NF}' | sed -n '3p'`
#echo $data
#2
war1=`ls -lrt /var/lib/jenkins/workspace/war-deploy-1/target/ | grep -i .war | awk -F "/"  '{print $NF}'`

sed 's/\(.*target\/\)\(.*war$\)/\2/'

ls -lrt /var/lib/jenkins/workspace/war-deploy-1/target/ | grep -i .war | awk '{print $NF}'
curl --silent -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText" | grep -i Building  | awk -F "/"  '{print $NF}' | awk 'END { print }'

#!/bin/bash

echo $WORKSPACE
dt=`date "+%Y-%m-%d-%H-%M"`
#ls -lrt $WORKSPACE/war-deploy-1/target/

war1=`ls -lrt /var/lib/jenkins/workspace/war-deploy-1/target/ | grep -i .war | awk '{print $9;}'`
#war2=`curl --silent -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText" | grep -i Building  | awk '{print $4;}' | sed -n '3p' | cut -d "/" -f8`
echo $war1

aws s3 cp /var/lib/jenkins/workspace/war-deploy-1/target/$war1 s3://hello-artifactory/$dt/$war1 --acl public-read-write


curl -i \
-u admin:password \
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data '{"extra_vars":{"ear_ver": "$(war1)"}}' "http://localhost/api/v2/job_templates/21/launch/"


