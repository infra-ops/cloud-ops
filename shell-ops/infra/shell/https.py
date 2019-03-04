PASS=`cat pass`
for i in `cat ip`
do
IP=`echo $i |cut -d ':' -f1`
PORT=`echo $i |cut -d ':' -f2`


#STATE=`sshpass -p redhat ssh -o StrictHostKeyChecking=no root@$IP netstat -plnt | awk '{print $4,$6}' | grep $PORT |  cut -d ':' -f4,5`
STATE=`sshpass -p '$PASS' ssh -t -v -o StrictHostKeyChecking=no root@$IP netstat -plnt | awk '{print $4,$6}' | grep $PORT | cut -d ':' -f4,5`
exit

#if [ $STATE == "LISTEN" ]


if [ -z "$STATE" ]
  then
      echo -e "port listening"
   else
      echo -e "port not Listening"
   fi
done

