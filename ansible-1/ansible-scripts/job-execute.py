#curl -k -u nik:iis123 -H 'Content-Type: application/json' -X POST -d /
#      '{"extra_vars:"{"war_ver": "$war1"}}' /
#       'http://localhost/api/v2/job_templates/20/launch'



#curl -s -k -u admin:password http://127.0.0.1/api/v2/job_templates/
#curl -s -k -u admin:password http://127.0.0.1/api/v2/job_templates/20/launch/


curl -f -k -H 'Content-Type: application/json' -XPOST \
    --user admin:password \
    http://127.0.0.1/api/v2/job_templates/20/launch/


curl -f -k -H 'Content-Type: application/json'  -XPOST \
   --user admin:password \
    -d   '{"extra_vars":{"ear_ver": $war1}}' \
    http://localhost/api/v2/job_templates/21/launch/



curl -i \
-u admin:password \	
-H "Accept: application/json" \
-H "Content-Type:application/json" \
-X POST --data '{"extra_vars":{"ear_ver": "$(war1)"}}' "http://localhost/api/v2/job_templates/21/launch/"






echo $WORKSPACE
echo $BUILD_NUMBER
dt=`date "+%Y-%m-%d-%H-%M"`


aws s3 cp /var/lib/jenkins/workspace/war-deploy-1/target/$war1 s3://hello-artifactory/$BUILD_NUMBER/ --recursive --acl public-read-write


war1=`curl -s -k -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText"  | tail -n 50 | sed -n '/upload/p' | egrep -o mavenproject1-1.0-SNAPSHOT.*war | cut -d " " -f1`
echo $war1


curl -s -k  \
     -u admin:password \
     -H "Accept: application/json" \
     -H "Content-Type:application/json" \
     -X POST --data '{"extra_vars":{"build_no":"'${BUILD_NUMBER}'","ear_ver":"'${war1}'"}}' "http://localhost/api/v2/job_templates/21/launch/"

