#!/bin/sh

## Schell script to create

delete_file=$1

for i in `cat $delete_file`
do
#rm -rf instance/$i; mkdir instance/$i
#cp variables.tf instance/$i/
cd instance/$i
terraform destroy -force -var "instance_name=$i"
echo "Instance $i destroyed"
cd ../..
done
#cd ../..
