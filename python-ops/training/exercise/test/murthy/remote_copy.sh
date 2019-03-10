#!/bin/shell
echo "" > copy_ok.txt
echo "" > copy_err.txt


for DATA  in `cat poz`
do
IP=`echo $DATA   |  awk -F":"   '{print $1}'`
#PORT=`echo $DATA |  awk -F":"    '{print $2}'`
USER=`echo $DATA |  awk -F":"    '{print $3}'`
PASS=`echo $DATA |  awk -F":"    '{print $4}'`
SSH="ssh -t -q -o ConnectTimeout=5 -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no"
SOURCE="/opt/ril_send"
DEST="/opt/ril_receive"
###############################################################################
if [ -f $SOURCEFILE ];then
echo "File found, preparing to transfer\n"
while read $IP
do
sshpass -p  $PASS  scp -r $SOURCE/* $SSH  $USER@$IP:$DEST
if [ $? -ne 0 ];then
sshpass -p "$PASS" rsync -e "$SSH" -av --progress $SOURCE/*  $USERR@$IP:$DEST
if [ $? -eq 0 ];then
echo "copid succesfully"
else
echo "copy  faliure on $IP" >> copy_err.txt
fi
else
echo "copy successfull on $IP " >> copy_ok.txt
fi
done
else
echo "File not found in the directory"
fi
done



