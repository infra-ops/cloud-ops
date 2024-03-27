cp comp2.txt comp3.txt
for i `cat comp1.txt`
do
grep -v $i comp3.txt > comp4.txt
cp comp4.txt comp5.txt
done
