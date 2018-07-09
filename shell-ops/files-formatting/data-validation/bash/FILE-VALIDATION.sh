#!/usr/bin/env bash

TERM=screen-256color
YMLDIR=/home/ubuntu/data-validation/yml
SQLDIR=/home/ubuntu/data-validation/sql

ALL_OK=1

print_err () {
	echo "$(tput setaf 1)$*$(tput sgr0)";
}

cd ${SQLDIR}

for F in $(egrep '^ +- +' ${YMLDIR}/FILE-LIST.yml | sed -e 's/^ *- *//')
do

	[ -r ${F} ] && {

		REPLACE_ERR=0
		DOLLAR_ERR=0
		LOCKING_ERR=0

                 [ "${F}" != "ddl/FL_P_JOB_PRCSS_DEF.sql" ] && {
                         if ! grep -qi REPLACE ${F}
                         then
                                 ALL_OK=0
                                 REPLACE_ERR=1
                         fi
               }






#		if ! grep -qi REPLACE ${F}
#		then
#			ALL_OK=0
#			REPLACE_ERR=1
#		fi









		[ "${F}" == "view/FL_P_EMPL_ATTR.sql" ] && {
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
			print_err "${F} : REPLACE, LOCKING and $ are absent"
		}||{

			[ ${REPLACE_ERR} -eq 1 ] && [ ${DOLLAR_ERR} -eq 1 ] && {
				print_err "${F} : REPLACE and $ are absent"
			}||{

				[ ${REPLACE_ERR} -eq 1 ] && [ ${LOCKING_ERR} -eq 1 ] && {
					print_err "${F} : REPLACE and LOCKING are absent"
				}||{

					[ ${DOLLAR_ERR} -eq 1 ] && [ ${LOCKING_ERR} -eq 1 ] && {
						print_err "${F} : LOCKING and $ are absent"
					}||{

						[ ${LOCKING_ERR} -eq 1 ] && print_err "${F} : LOCKING is absent"

						[ ${REPLACE_ERR} -eq 1 ] && print_err "${F} : REPLACE is absent"

						[ ${DOLLAR_ERR} -eq 1 ] && print_err "${F} : $ is absent"

					} 

				} 

			} 

		} 

	} # if -r ${F}
	
done

[ ${ALL_OK} -eq 1 ] && {
	echo "All files are OK"
}
