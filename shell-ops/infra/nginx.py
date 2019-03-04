#!/bin/sh
SERVER_IP='xxxxx'
DATE=`date '+%Y-%m-%d %H:%M:%S'`

port=`netstat -ntupl | grep 80`
if [ -z "$port" ]
then
echo "nginx critical";
#python rest.py 192.168.10.36
#python rest.py $1
#retval=2;

curl "https://url/api/now/table/incident" \
--request POST \
--header "Accept:application/json" \
--header "Content-Type:application/json" \
--data "{\"short_description\":\"Nginx is down on $SERVER_IP AT $DATE \",\"description\":\"down\"}" \
--user 'xxx':'xxxxx'



exit 2
else
echo "nginx ok";
#retval=0;
fi
exit 0
#$retval;
