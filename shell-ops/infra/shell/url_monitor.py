#!/bin/bash
#Checking urls from urls.txt
#MAddr="vishal.pisal@ril.com"
#TIME=`date +%d-%m-%Y_%H.%M.%S`

FILE_UP="LinkUP_$(date +%F).txt"
FILE_Down="LinkDown_$(date +%F_%H:%M:%S).txt"



for url in `awk '{print $1}' urls.txt`
do
    /usr/bin/wget -t 0 --spider --no-check-certificate $url > wget.output  2>&1
    HTTPCode=`(/usr/bin/wget -t 0 --spider --no-check-certificate $url) 2>&1 | grep HTTP| tail -1|cut -c 41-43`
        ENV=`(grep $url urls.txt | awk '{print $2}')`
        echo $HTTPCode
        E1=`/bin/grep -ise  'refused' -ise 'failed'  wget.output`
        if [ "$E1" != "" ] || [ $HTTPCode -ge 500 ]
then
        echo "$url is DOWN"  >> $FILE_Down
else
        echo " $url is UP "  >> $FILE_UP
fi
done

cat body.txt | mailx -s "URL MONITORING STATUS REPORT:" -r no-reply@ril.com  -a $FILE_UP no-reply@ril.com



