#!/usr/bin/env bash

TERM=screen-256color
YMLDIR=/home/ubuntu/data-validation/yml
SQLDIR=/home/ubuntu/data-validation/sql/ddl


################################################################################
#  
#  Begin declare functions 
#
################################################################################

print_err () {
	echo "$(tput setaf 1)$*$(tput sgr0)";
}

check_char () {

	F=${1}

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
}

check_varchar () {

	F=${1}

	VARCHAR_OK=1
	while read VCLINE
	do
		VCVAL=$(echo ${VCLINE}|awk '{print $3}'|cut -d\( -f2|tr -d ')')
		[ ${VCVAL} -lt 3 ] && {
			VARCHAR_OK=0
			ALL_OK=0
			print_err "Wrong varchar present at line ${VCLINE}"
		}
	
	done < <(grep -n " VARCHAR" ${F}|tr -s ' ')
	
	[ ${VARCHAR_OK} -eq 1 ] && {
		echo "'VARCHAR FORMAT' is correct"
	}
}

check_varchar19 () {

	F=${1}

	VARCHAR_OK=1
	while read VCLINE
	do
		VCVAL=$(echo ${VCLINE}|awk '{print $2}'|cut -d\( -f2|tr -d ')')
		[ ${VCVAL} -lt 3 ] && {
			VARCHAR_OK=0
			ALL_OK=0
			print_err "Wrong varchar present at line ${VCLINE}"
		}
	
	done < <(grep -n " VARCHAR" ${F}|tr -s ' ')
	
	[ ${VARCHAR_OK} -eq 1 ] && {
		echo "'VARCHAR FORMAT' is correct"
	}
}


check_dateformat () {

	F=${1}

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
}

check_pi () {

	F=${1}

	if grep -q "PRIMARY INDEX" ${F} 
	then
		echo "'PI' is present"
	else
		print_err "'PI' is absent"
		ALL_OK=0
	fi

}

check_unique () {
	
	F=${1}

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
}

check_no () {

	F=${1}

	NO_CHECK=$(egrep -n "FALLBACK|BEFORE JOURNAL|AFTER JOURNAL" ${F} | egrep -v "NO FALLBACK|NO BEFORE JOURNAL|NO AFTER JOURNAL")
	[ ! -z "${NO_CHECK}" ] && {

		print_err "'NO' absent at line $(echo ${NO_CHECK} | sed 's/, */,/g' | tr , '\n')"
		ALL_OK=0
	}||{
		echo "'NO' is present in all"
	}
}

check_no_19 () {

	F=${1}

	NO_CHECK=$(egrep -n "FALLBACK|BEFORE JOURNAL|AFTER JOURNAL" ${F} | egrep -v "NO FALLBACK|NO BEFORE JOURNAL|NO AFTER JOURNAL")
	[ ! -z "${NO_CHECK}" ] && {

		print_err "'NO' absent at line $(echo ${NO_CHECK})"
		ALL_OK=0
	}||{
		echo "'NO' is present in all"
	}
}

check_notnull () {

	F=${1}

	PRIMINDVAL=$(grep "UNIQUE PRIMARY INDEX" ${F}|cut -d\( -f2| cut -d\) -f1)
	if ! grep ${PRIMINDVAL} ${F} | grep -v "UNIQUE PRIMARY INDEX" | grep -q "NOT NULL"
	then
		print_err "'NOT NULL' absent"
		ALL_OK=0
	else
		echo "'NOT NULL' present"
	fi
}


check_notnull_19 () {

	# CHECK NOT NULL FOR MULTISET TABLE  LIKE test-19
	################################################################

	F=${1}
	
	PRIMINDVAL=$(grep -i "PRIMARY INDEX" ${F}|cut -d\( -f2| cut -d\) -f1)
	if ! grep ${PRIMINDVAL} ${F} | grep -iv "PRIMARY INDEX" | grep -iq "NOT NULL"
	then
		print_err "'NOT NULL' absent"
		ALL_OK=0
	else
		echo "'NOT NULL' present"
	fi
}


################################################################################
#  
#  End declare functions 
#
################################################################################



######################################
# Main loop 
#
######################################

cd ${SQLDIR} 
for F in $(egrep '^ +- +' ${YMLDIR}/f11.yml | sed -e 's/^ *- *//')
do

	[ -r ${F} ] && {
	
		ALL_OK=1
		
		echo -e "\n==========================="
		echo "Check file ${F}"
		echo "==========================="
		
		# Check NO
		##############
		[ "${F}" == "test-19.sql" ] && {
			check_no_19 ${F} 
		}||{
			check_no ${F}
		}



		# Check UNIQUE
		##############
		check_unique ${F}


		# Check PI
		##############
		check_pi ${F}


		# Check date format
		#####################
		check_dateformat ${F}


		# Check VARCHAR 
		################
		[ "${F}" == "test-19.sql" ] && {
			check_varchar19 ${F}
		}||{
			check_varchar ${F}
		}

		
		# Check CHAR 
		################
		check_char ${F}


		# Check not null
		##################
		[ "${F}" == "test-19.sql" ] && {
			check_notnull_19 ${F}
		}||{
			check_notnull ${F}
		}


		# CHECK FOR TEST-19.SQL
		################################################################
		[ "${F}" == "test-19.sql" ] && {
		
			if grep -iq "MULTISET VOLATILE" ${F}
			then
				if grep -q "on commit preserve rows" ${F}
				then
					echo "MULTISET VOLATILE WITH COMMIT PRESERVE ROWS PRESENT IN TEST-19.SQL"
				else
					print_err "'MULTISET VOLATILE WITH COMMIT PRESERVE ROWS NOT PRESENT IN TEST-19.SQL'"
					exit
				fi
			fi
		}

		
		[ ${ALL_OK} -eq 1 ] && {
			echo -e "\nAll is OK for file ${F}"
		}
	
	} # if -r ${F}

done
