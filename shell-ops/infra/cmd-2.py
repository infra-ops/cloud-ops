port=`ps -ef | pgrep apache2 |wc -l`
if [ -z "$port" ]
then
echo "CRITICAL! Syntax: ./check_apache.sh apache CRITICAL";
exit 2

else
if [ "$port" -le "6" ]
then
echo "WARNING - Number of process is $port";
exit 1

else
echo "No Of Running Apache Process is :" "$port";
exit 0
fi
fi



port=`netstat -ntupl | grep 8080`
if [ -z "$port" ]
then
echo "tomcat critical";
retval=2;
else
echo "tomcat ok";
retval=0;
fi
exit
$retval;

