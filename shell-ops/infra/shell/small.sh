#!/bin/bash
a=8
if (( $a >= 9 )); then
   echo "score is correct"
   exit 0
else
   echo "score is incorrect"
   exit 1
fi

