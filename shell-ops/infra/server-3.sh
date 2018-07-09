#!/bin/bash

TO="xxxxx"
FROM="xxxxxx"
SUBJECT="SERVER STATUS"
BODY="SERVICE STATUS"



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

        VALUE=$(sshpass -p ${PASS} ssh -n -o StrictHostKeyChecking=no  ${USER}@${IP}  "${CMD1}" | head -2 | tail -1)
        PERCENTAGE=$(sshpass -p ${PASS} ssh -n -o StrictHostKeyChecking=no  ${USER}@${IP}  "${CMD2}" )

#               echo PERCENTAGE ${PERCENTAGE}
#               echo VALUE ${VALUE}

        if [ ${PERCENTAGE} -lt 90 ]; then

           [ ! -f $DT.log_ok.csv ] && printf "Server ip,Date,Time,Value,Percentage\n" > $DT.log_ok.csv

        echo  -e "${IP} ,$DT1 ,$TM , ${VALUE} ,${PERCENTAGE}"
        echo  -e "${IP} ,$DT1 ,$TM , ${VALUE} ,${PERCENTAGE}" >> $DT.log_ok.csv

        else

           #echo "${IP} ---> ${status}" >> $FILE_STATUS | mailx -s ${SUBJECT} ${TO_ADDRESS} --r ${FROM_ADDRESS}

           [ ! -f $DT.log_err.csv ] && printf "Server ip,Date,Time,Value,Percentage\n" > $DT.log_err.csv

           echo  -e "${IP},${DT1},${TM},${VALUE},${PERCENTAGE}" >> $DT.log_err.csv
        fi

    }

done < <(egrep "host|user|pass|cmd-1|cmd-2" ${NODESFILE} )





ATTACHMENT="$DT.log_ok.csv"


[ -f $ATTACHMENT ] && {

        #echo "Hi, this is a csv file" | mailx -s ${SUBJECT} -a $DT.log_ok.csv ${TO}

#       mail -s "$SUBJECT" "$TO" < $ATTACHMENT
        echo "server status" |  mutt -a "$ATTACHMENT" -s "service status" -- $TO
}

