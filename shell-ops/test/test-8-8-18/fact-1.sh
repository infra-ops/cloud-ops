echo -n " enter a no. "
read n
i=1
k=1
until [ $i -gt $n ]
do
k=`expr $k \* $i `
i=`expr $i + 1 `
done
echo " factorial of $n is $k "
