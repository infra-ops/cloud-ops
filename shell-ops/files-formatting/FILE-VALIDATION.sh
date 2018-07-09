#!/usr/bin/env bash

ALL_OK=1
for F in $(egrep '^ +- +' ../yml/FILE-LIST.yml | sed -e 's/^ *- *//')
do

[ -r ${F} ] && {

REPLACE_ERR=0
DOLLAR_ERR=0
LOCKING_ERR=0

[ "${F}" != "../sql/ddl/FL_P_JOB_PRCSS_DEF.sql" ] && {
if ! grep -qi REPLACE ${F}
then
ALL_OK=0
REPLACE_ERR=1
fi
}      

[ "${F}" == "../sql/view/FL_P_EMPL_ATTR.sql" ] && {
if ! grep -qi LOCKING ${F}
then
ALL_OK=0
LOCKING_ERR=1
fi
}      

if ! grep -q "\\$" ${F}
then
ALL_OK=0
DOLLAR_ERR=1
fi


[ ${REPLACE_ERR} -eq 1 ] && [ ${DOLLAR_ERR} -eq 1 ] && [ ${LOCKING_ERR} -eq 1 ] && {
echo "${F} : REPLACE, LOCKING and $ are absent"
}||{

[ ${REPLACE_ERR} -eq 1 ] && [ ${DOLLAR_ERR} -eq 1 ] && {
echo "${F} : REPLACE and $ are absent"
}||{

[ ${REPLACE_ERR} -eq 1 ] && [ ${LOCKING_ERR} -eq 1 ] && {
echo "${F} : REPLACE and LOCKING are absent"
}||{

[ ${DOLLAR_ERR} -eq 1 ] && [ ${LOCKING_ERR} -eq 1 ] && {
echo "${F} : LOCKING and $ are absent"
}||{

[ ${LOCKING_ERR} -eq 1 ] && echo "${F} : LOCKING is absent"

[ ${REPLACE_ERR} -eq 1 ] && echo "${F} : REPLACE is absent"

[ ${DOLLAR_ERR} -eq 1 ] && echo "${F} : $ is absent"
}  
}
}          
}          
}          

done

[ ${ALL_OK} -eq 1 ] && {
echo "All files are OK"
}
