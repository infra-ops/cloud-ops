
for i in `cat pod`
do
IP=`echo $i | awk -F":" '{print $1}'`
#PORT=`echo $i |awk -F":" '{print $2}'`
USER=`echo $i | awk -F":" '{print $3}'`
PASS=`echo $i| awk -F":" '{print $4}'`
op=`sshpass -p $PASS ssh -o StrictHostKeyChecking=no $USER@$IP  hostname`
if [ $? -eq 0 ];then
echo "$i ---> $op " >> host_ok.txt
else
echo "$i ---> none "  >> host_err.txt
fi
done
