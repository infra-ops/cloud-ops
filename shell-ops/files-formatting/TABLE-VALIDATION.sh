#!/usr/bin/env bash
TERM=screen-256color
print_err () {
	echo "$(tput setaf 1)$*$(tput sgr0)";
}

MULTISET_notnull () {
	# CHECK NOT NULL FOR MULTISET TABLE  LIKE MULTISET
	################################################################
	[ -f ../ddl/MULTISET.sql ] && {
	
		F="../ddl/MULTISET.sql"
		PRIMINDVAL=$(grep -i "PRIMARY INDEX" ${F}|cut -d\( -f2| cut -d\) -f1)
		if ! grep ${PRIMINDVAL} ${F} | grep -iv "PRIMARY INDEX" | grep -iq "NOT NULL"
		then
			print_err "'NOT NULL' absent"
			ALL_OK=0
		else
			echo "'NOT NULL' present"
		fi
	}
}
for F in $(egrep '^ +- +' ../yml/TABLE-LIST.yml | sed -e 's/^ *- *//')
do
	[ -r ${F} ] && {
	
		ALL_OK=1
		
		echo -e "\n==========================="
		echo "Check file ${F}"
		echo "==========================="
		
		# Check NO
		##############
		NO_CHECK=$(egrep -n "FALLBACK|BEFORE JOURNAL|AFTER JOURNAL" ${F} | egrep -v "NO FALLBACK|NO BEFORE JOURNAL|NO AFTER JOURNAL")
		[ ! -z "${NO_CHECK}" ] && {
			[ "${F}" == "MULTISET.sql" ] && {
				print_err "'NO' absent at line $(echo ${NO_CHECK})"
			}||{
				print_err "'NO' absent at line $(echo ${NO_CHECK} | sed 's/, */,/g' | tr , '\n')"
			}
			ALL_OK=0
		}||{
			echo "'NO' is present in all"
		}
		
		# Check UNIQUE
		##############
		if grep -q "SET TABLE" ${F} 
		then
			if grep -q "UNIQUE PRIMARY" ${F}
			then
				echo "'SET WITH UNIQUE' is present"	
			else
				print_err "'SET WITH UNIQUE' is not present, exit program !"	
				exit
			fi
		fi
		
		# Check PI
		##############
		if grep -q "PRIMARY INDEX" ${F} 
		then
			echo "'PI' is present"
		else
			print_err "'PI' is absent"
			ALL_OK=0
		fi
		
		
		# Check date format
		#####################
		DATEFORMAT_OK=1
		while read DFLINE
		do
			if ! echo "${DFLINE}"| grep -q 'YYYY-MM-DD'
			then
				DATEFORMAT_OK=0
				ALL_OK=0
				print_err "Date format is incorrect at line ${DFLINE}"
			fi
		done < <(grep -n " DATE FORMAT" ${F}|tr -s ' ')
		
		[ ${DATEFORMAT_OK} -eq 1 ] && {
			echo "'DATE FORMAT' is correct"
		}
		
		
		# Check VARCHAR 
		################
		VARCHAR_OK=1
		while read VCLINE
		do
			[ "${F}" == "../ddl/MULTISET.sql" ] && {
				VCVAL=$(echo ${VCLINE}|awk '{print $2}'|cut -d\( -f2|tr -d ')')
			}||{
				VCVAL=$(echo ${VCLINE}|awk '{print $3}'|cut -d\( -f2|tr -d ')')
			}
			[ ${VCVAL} -lt 3 ] && {
				VARCHAR_OK=0
				ALL_OK=0
				print_err "Wrong varchar present at line ${VCLINE}"
			}
		
		done < <(grep -n " VARCHAR" ${F}|tr -s ' ')
		
		[ ${VARCHAR_OK} -eq 1 ] && {
			echo "'VARCHAR FORMAT' is correct"
		}
		
		
		# Check CHAR 
		################
		CHAR_OK=1
		while read CLINE
		do
			CVAL=$(echo ${CLINE}|awk '{print $3}'|cut -d\( -f2|tr -d ')')
			[ ${CVAL} -gt 3 ] && {
				CHAR_OK=0
				ALL_OK=0
				print_err "Wrong char present at line ${CLINE}"
			}
		
		done < <(grep -n " CHAR(" ${F}|tr -s ' ')
		
		[ ${CHAR_OK} -eq 1 ] && {
			echo "'CHAR FORMAT' is correct"
		}
		
		
		# Check NOT NULL FOR SET TABLE LIKE test-17 test-18
		################################################################
		[ "${F}" == "../ddl/FL_P_JOB_PRCSS_DEF.sql" ] || [ "${F}" == "../ddl/FL_P_JOB_PRCSS_DEF-1.sql" ] && {
			PRIMINDVAL=$(grep "UNIQUE PRIMARY INDEX" ${F}|cut -d\( -f2| cut -d\) -f1)
			if ! grep ${PRIMINDVAL} ${F} | grep -v "UNIQUE PRIMARY INDEX" | grep -q "NOT NULL"
			then
				print_err "'NOT NULL' absent"
				ALL_OK=0
			else
				echo "'NOT NULL' present"
			fi
		}
		
		
		############
		# This is the function
		#################
		MULTISET_notnull
		# CHECK NOT NULL FOR MULTISET TABLE  LIKE MULTISET
		################################################################
#		[ "${F}" == "MULTISET.sql" ] && {
#
#			PRIMINDVAL=$(grep -i "PRIMARY INDEX" ${F}|cut -d\( -f2| cut -d\) -f1)
#			if ! grep ${PRIMINDVAL} ${F} | grep -iv "PRIMARY INDEX" | grep -iq "NOT NULL"
#			then
#				print_err "'NOT NULL' absent"
#				ALL_OK=0
#			else
#				echo "'NOT NULL' present"
#			fi
#		}
		
		
		# CHECK FOR TEST-19.SQL
		################################################################
		[ "${F}" == "../ddl/MULTISET.sql" ] && {
		
			if grep -iq "MULTISET VOLATILE" ${F}
			then
				if grep -q "on commit preserve rows" ${F}
				then
					echo "MULTISET VOLATILE WITH COMMIT PRESERVE ROWS PRESENT"
				else
					print_err "'MULTISET VOLATILE WITH COMMIT PRESERVE ROWS NOT PRESENT'"
					exit
				fi
			fi
		}
		
		[ ${ALL_OK} -eq 1 ] && {
			echo -e "\nAll is OK for file"
		}
	
	} # if -r ${F}
done
