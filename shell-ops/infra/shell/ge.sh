#!/bin/bash

s2=99
if [ $s2 -ge 99 ]; then
	echo "score is correct"
	exit 0
else
       echo "score is incorrect"
       exit 1
fi

