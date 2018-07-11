#!/bin/bash


cat pox | while read i

do


#ping -q -c5 "$i" > /dev/null

fping "$i"  >  /dev/null

if [ $? -eq 0 ]

then

   echo "$i is alive"
   echo "$i is alive" >> ping_ok.txt

else

   echo "$i is  dead"
   echo "$i is  dead" >> ping_err.txt

fi

done
