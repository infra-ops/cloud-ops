#!/bin/bash


[ -z "${1}" ] || [ "${1}" != "p4.yml" ] && {
	echo "Usage: ${0} p4.yml"
	exit
}

P4FILE=${1}

[ ! -f "${P4FILE}" ] && {
	echo "Can't find ${P4FILE} !"
	exit
}

PLUGINDIR="/var/lib/jenkins/plugins"

while read HTTPLINE
do
    
    HPIFILE=$(basename ${HTTPLINE} )
    printf " - name: %s\n   get_url:\n     url: %s\n     dest: %s/%s\n   become: yes\n" ${HPIFILE} ${HTTPLINE} ${PLUGINDIR} ${HPIFILE}

done < <(grep http ${P4FILE} | sed -e "s/^ *- *//g")  
