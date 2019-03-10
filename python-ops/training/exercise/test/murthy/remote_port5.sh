#!/bin/shell
for DATA  in `cat pod`
do
IP=`echo $DATA   |  awk -F":"   '{print $1}'`
PORT=`echo $DATA |  awk -F":"    '{print $2}'`
USER=`echo $DATA |  awk -F":"    '{print $3}'`
PASS=`echo $DATA |  awk -F":"    '{print $4}'`
###############################################################################
sshpass -p $PASS  ssh -l $USER $IP   StrictHostKeyChecking=no    "netstat -plan | grep -w $PORT | grep -iE '(LISTEN|tcp|udp)'"

if [ $? = 0 ]; then
echo -e "$IP \t \t $PORT  \t \t   listening  " >> port_ok.txt
else
echo -e "$IP \t \t $PORT \t \t   not listening  " >> port_err.txt
fi
done

