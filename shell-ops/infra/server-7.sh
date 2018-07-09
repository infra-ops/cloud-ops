#!/bin/bash

TO="xxxx@gmail.com"
FROM="xxxxx@gmail.com"
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


make_xlsx () {

CSVFILE=${1}
XLSXFILE="$(echo ${CSVFILE}|cut -d. -f1-2).xlsx"
( cat <<-EOS

#!/usr/bin/env python

import os
import csv
import sys

from openpyxl import Workbook

reload(sys)
sys.setdefaultencoding('utf8')

if __name__ == '__main__':
    workbook = Workbook()
    worksheet = workbook.active
    csvfile="${CSVFILE}"
    excelfile="${XLSXFILE}"

    #worksheet = workbook.add_sheet('Disk') 
    #with open('TEST.CSV', 'r') as f:
    with open(csvfile, 'r') as f:
        reader = csv.reader(f)
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                for idx, val in enumerate(col.split(',')):
                    cell = worksheet.cell(row=r+1, column=c+1)
                    cell.value = val

    workbook.save(excelfile)
EOS
) | python 

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

		done < <(sshpass -p ${PASS} ssh -n -o StrictHostKeyChecking=no  ${USER}@${IP}  "${CMD1}" | tail -n +2)
	}

done < <(egrep "host|user|pass|cmd-1|cmd-2" ${NODESFILE} )


# Send mail
[ -f $DT.log_ok.csv ] && {
	echo "Write ok .xlsx file"
	make_xlsx $DT.log_ok.csv  # make file: $DT.log_ok.xlsx

	# mail attachment $DT.log_ok.xlsx
}

[ -f $DT.log_err.csv ] && {
	echo "Write error .xlsx file"
	make_xlsx $DT.log_err.csv  # make file: $DT.log_err.xlsx

	# mail attachment $DT.log_err.xlsx
}
