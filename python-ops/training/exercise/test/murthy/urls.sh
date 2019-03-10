FILE_UP="LinkUP_$(date +%F).txt"
FILE_Down="LinkDown_$(date +%F_%H:%M:%S).txt"
BODY=/tmp/body.txt


echo "Greetings!!!" > $BODY
echo
echo "        It has been observed that below URL is not accessible from the application monitoring server" >> $BODY


for i in `cat url.txt`
do
#if curl -s --head $i | grep "200 OK" > /dev/null
if wget -t 0 --spider --no-check-certificate $i 2>&1 | grep HTTP| tail -1|cut -c 41-43 | grep 200 > /dev/null
then
        echo -e "URL: $i" >> $FILE_UP
else
        echo -e "URL: $i" >> $BODY

fi
        done

echo "        Hence, request you to check this on “HIGH PRORITY. " >> $BODY

echo "       Thanks & Regards," >> $BODY
echo "       RJIL APPS SUPPORT" >> $BODY

cat /tmp/body.txt | mailx -s "JIO URL MONITORING STATUS REPORT:" -r no-reply@ril.com  vishal.pisal@ril.com

