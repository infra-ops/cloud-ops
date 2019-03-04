sed -i "37i <role rolename="manager-gui"/>" /opt/AIC-CLOUDS/tomcat/conf/tomcat-users.xml
sed -i "38i <role rolename="manager-script"/>" /opt/AIC-CLOUDS/tomcat/conf/tomcat-users.xml
sed -i "39i <role rolename="manager-jmx"/> " /opt/AIC-CLOUDS/tomcat/conf/tomcat-users.xml
sed -i "40i <user username="tomcat" password="password" roles="manager-gui,manager-script,manager-jmx,manager-status,admin-gui,admin-script"/>" /opt/AIC-CLOUDS/tomcat/conf/tomcat-users.xml

sed -i 's#8080#9090#' /opt/AIC-CLOUDS/tomcat/conf/server.xml
sed -i 's#8005#9005#' /opt/AIC-CLOUDS/tomcat/conf/server.xml
/opt/AIC-CLOUDS/tomcat/bin/startup.sh


TO_ADDRESS="xxxxx@gmail.com"
FROM_ADDRESS="xxxxx@gmail.com"
SUBJECT1="SUCCESSFUL"
SUBJECT2="FAILED"
mkdir -p /opt/back

if [ $? = 0 ]; then

cp -rvf /opt/test1.txt /opt/back/test2.txt

if [ $? = 0 ]; then

status1=`curl -sI http://www.google.com|grep 302 | awk '{print $2;}'`

if [[ $status1 == 302 ]]; then

echo ${status1} | mailx -s ${SUBJECT1} ${TO_ADDRESS} -- -r ${FROM_ADDRESS}
else

echo ${status1} | mailx -s ${SUBJECT2} ${TO_ADDRESS} -- -r ${FROM_ADDRESS}

fi
fi
fi

mvn clean install

mvn tomcat7:deploy


alias tom='cd /opt/tomcat/bin/'
alias mav='cd /usr/local/devlopment/maven/'
