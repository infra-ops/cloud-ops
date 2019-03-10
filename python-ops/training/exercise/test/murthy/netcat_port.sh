pass=`cat /opt/sudipta/pws`
admin="idcadm"
#port=`cat /opt/sudipta/listen`
for i in `cat /opt/sudipta/ips2`
do
ip=`echo $i |cut -d ':' -f1`
port=`echo $i |cut -d ':' -f2`
#####################################################################################
#op=`sshpass -p $pass ssh -o StrictHostKeyChecking=no $admin@$ip netstat -plant | awk '{print $4}' |grep -w $i | cut -d ':' -f4,5 | sort -u`
op=`nc -z $ip $port`
if [ -z "$op" ];then
        echo -e "$ip \t \t $port \t \t  NOT listening  " >> port_err.txt
        else
        echo -e "$ip \t \t $port \t \t  Listening  " >> port_OK.txt
        fi
done
