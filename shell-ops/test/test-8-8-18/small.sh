echo "enter nos"
read a b c

n=$a

   if [ $b -lt $n ]; then
      n=$b
 fi

   if [ $c -lt $n ]; then
   n=$c
 fi
  echo "smallest of $a $b $c is $n"
