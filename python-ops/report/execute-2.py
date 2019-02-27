#!/bin/bash

cmd()
{


cmd1=$(hostname -I | cut -d " " -f1)
cmd2=$(uname -n)


cmd3=$(ls -ld /opt/data);
cmd4=$(ls -ld /opt/apps/solr/server/logs);
cmd5=$(ls -ld /opt/apps/zookeeper/server/logs);
cmd6=$(cat /opt/apps/solr/bin/solr.in.sh | grep -i SOLR_LOGS_DIR= | cut -d "=" -f2 | sed 's/.$//; s/^.//');
cmd7=$(cat /opt/apps/zookeeper/conf/zookeeper-env.sh  | grep -i ZOO_LOG_DIR= | sed -n '2p' | cut -d "="  -f2 |  sed 's/.$//; s/^.//');
cmd8=$(cat /opt/apps/solr/server/resources/log4j.properties | grep -i solr.log | sed -n '1p' | cut -d "="  -f2)

echo "${cmd1}"
echo "${cmd2}"
echo "${cmd3}"
echo "${cmd4}"
echo "${cmd5}"
echo "${cmd6}"
echo "${cmd7}"
echo "${cmd8}"




}

cmd


