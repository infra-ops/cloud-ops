n=7
i=2
f=0

while [ $i -le $(($n /2)) ]; do
  if [ $((n%i)) -eq 0 ]; then
   f=1
   break
   fi
   i=$(($i+1))
 done  

if [ $f -eq 1 ]; then
   echo "no"
else
   echo "yes"
fi
