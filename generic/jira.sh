cd /opt/store ; wget https://www.atlassian.com/software/jira/downloads/binary/atlassian-jira-6.4.10-x64.bin ; chmod 777 atlassian-jira-6.4.10-x64.bin

apt-get install mysql-server
#mysql_secure_installation
echo "create database jiradb  character set utf8" |mysql  -uroot -ppassword
echo "create user 'jira'@'localhost' identified by 'jira123'" | mysql -uroot -ppassword
echo "GRANT ALL Privileges ON jiradb.* TO 'jira'@'localhost' IDENTIFIED by 'jira123' with grant option"  | mysql -uroot -ppassword
echo "flush privileges" | mysql -uroot -ppassword
echo "show databases" | mysql -uroot -ppassword


