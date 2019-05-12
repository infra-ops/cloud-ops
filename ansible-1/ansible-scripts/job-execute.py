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




