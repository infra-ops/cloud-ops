#!/bin/bash

##########SOURCE DIRECTORY####

##DYEAR=`date "+%Y"`
#DYM=`date "+%Y%m"`
#DDATE=`date --date='yesterday' '+%Y%m%d'`
#DPATHSTC="/FI_GW_TDR/FI_FT/$DYEAR/$DYM/$DDATE/STC/*-STC.tdr"
#DPATHSTV="/FI_GW_TDR/FI_FT/$DYEAR/$DYM/$DDATE/STV/*-STV.tdr"


##########FILE NAMES##########

#DATE=`date "+%d-%m-%Y"`
#REQUEST="$DDATE-REQUEST"
#RESPONSE="$DDATE-RESPONSE"
#MIS="$DDATE-MIS-FI-FT"

##########DESTINATION DIRECTORY######

#SMONTH=`date | awk '{print $2}'`
#if [ ! -d "$SMONTH" ]
#then
#mkdir -p /FI_GW_FT_DETAILS/$SMONTH
#fi
#SOURCEPATH="/FI_GW_FT_DETAILS/$SMONTH"


###### REQUEST FROM VENDOR ######

cd /FI_GW_TDR/FI_FT/2013/201303/20130310/STC/
#for SEP in `find . -name "*-STC.tdr" | awk -F"/" '{print $2}'`
for SEP in `ls *-STC.tdr`
do
PROSEESS=`cut -b 30-35 $SEP`
if [ $PROSEESS -eq '401000' ]
then
RRN=`cut -b 71-82 $SEP`
FACCOUNT=`cut -b 118-127 $SEP`
TACCOUNT=`cut -b 137-146 $SEP`
echo $RRN $FACCOUNT $TACCOUNT >> /FI_GW_FT_DETAILS/Mar/20130310-REQUEST
fi
done


####### RESPONSE FROM BANK #######

cd /FI_GW_TDR/FI_FT/2013/201303/20130310/STV/
for file in `ls *-STV.tdr`
#for SEP in `find . -name "*-STV.tdr" | awk -F"/" '{print $2}'`
do
PROCESS=`awk 'FNR>1' $file | cut -b 12-17`
if [ $PROCESS -eq '401000' ]
then
VCODE=`basename $file | cut -b 1-2`
AMOUNT=`awk 'FNR>1' $file | cut -b 18-29`
DDMMYY=`awk 'FNR>1' $file | cut -b 30-35`
TTMM=`awk 'FNR>1' $file | cut -b 36-41`
MMC=`awk 'FNR>1' $file | cut -b 46-49`
RRN=`awk 'FNR>1' $file | cut -b 50-61`
RESCODE=`awk 'FNR>1' $file | cut -b 62-64`
TERID=`awk 'FNR>1' $file | cut -b 65-72`
BCODE=`awk 'FNR>1' $file | cut -b 236-241`
echo $PROCESS $RESCODE $VCODE $BCODE $MMC $DDMMYY $TTMM $TERID $AMOUNT $RRN >> /FI_GW_FT_DETAILS/Mar/20130310-RESPONSE
fi
done

####### COMPARE REQUSET AND RESPONSE #######

#LINECOUNT=`wc -l "$SOURCEPATH/$REQUEST" | awk '{print $1}'`
#LINENUM=1
#while [ $LINENUM -le $LINECOUNT ]
#do
#LINE=`sed -n $LINENUM'p' "$SOURCEPATH/$REQUEST"`
#RR_no=`echo $LINE|awk '{print $1}'`
#LINE2=`grep $RR_no "$SOURCEPATH/$RESPONSE"`
#echo "$LINE2 $LINE" >> $SOURCEPATH/$MIS
#LINENUM=`expr $LINENUM + 1`
#done

