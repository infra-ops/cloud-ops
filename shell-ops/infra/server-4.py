#!/bin/bash

TO="xxxxxxx"
FROM="xxxxxxx"
SUBJECT="xxxxx"
BODY="xxxxxx"



#echo > $DT.log_ok.csv
#echo > $DT.log_err.csv

DT=`date '+%d-%m-%Y-%H-%M-%S'`
DT1=`date '+%d-%m-%Y'`

TM=`date +"%r"`

[ -z "${1}" ] && {
    echo "Usage: ${0} n6.yml"
    exit
}

#set -x

NODESFILE=${1}
NODEINFOLINE=0


while read NODEINFO
do

    #echo $NODEINFO

    (( NODEINFOLINE++ ))

    [ ${NODEINFOLINE} == 1 ] && {
        IP=$(echo ${NODEINFO}|tr -d " " | cut -d: -f2)
    }

    [ ${NODEINFOLINE} == 2 ] && {
        USER=$(echo ${NODEINFO}|tr -d " " | cut -d: -f2)
    }

    [ ${NODEINFOLINE} == 3 ] && {
        PASS=$(echo ${NODEINFO}| tr -d " " | cut -d: -f2)
    }

    [ ${NODEINFOLINE} == 4 ] && {
        CMD1=$(echo ${NODEINFO}|cut -d: -f2)
    }



    [ ${NODEINFOLINE} == 5 ] && {

        CMD2=$(echo ${NODEINFO}|cut -d: -f2)
        NODEINFOLINE=0

        #sshpass -p ${PASS} ssh -n -o StrictHostKeyChecking=no  ${USER}@${IP}  "${CMD1} ; ${CMD2}"

        FIRSTLINE=0
        while read DFLINE
        do

            (( FIRSTLINE++ ))

            PERCENTAGE=$(echo ${DFLINE}| awk '{ print $5}' | cut -d% -f1)

            [ ${PERCENTAGE} -lt 90 ] && {
                WRITETOCSV="$DT.log_ok.csv"
            }||{
                WRITETOCSV="$DT.log_err.csv"
            }

            [ ! -f ${WRITETOCSV} ] && printf "Server ip,Date,Time,Value,Percentage\n" > ${WRITETOCSV}

            [ ${FIRSTLINE} -eq 1 ] && {
                echo  -e "${IP} ,$DT1 ,$TM , ${DFLINE} ,${PERCENTAGE}" >> ${WRITETOCSV}
            }||{
                echo  -e ",,, ${DFLINE} ,${PERCENTAGE}" >> ${WRITETOCSV}
            }

        done < <(sshpass -p ${PASS} ssh -n -o StrictHostKeyChecking=no  ${USER}@${IP}  "${CMD1}" | tail -n+2)
    }

done < <(egrep "host|user|pass|cmd-1|cmd-2" ${NODESFILE} )


ATTACHMENT="$DT.log_ok.csv"

# At this point send mail
[ -f $DT.log_ok.csv ] && {
#    echo "Log file written"
     echo "server status" |  mutt -a "$ATTACHMENT" -s "service status" -- $TO



}

[ -f $DT.log_err.csv ] && {
    echo "Error"
}
