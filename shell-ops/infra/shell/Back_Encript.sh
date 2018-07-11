#!/bin/bash

### Purpose #####

####Take the Backup and Encrypt the Files via Date and Vendor Vise

Date=`date +'%Y%m%d'`
SrcDir=`ls /Itgs_TDR`
Source="/Itgs_TDR/$SrcDir"
Destination="/Back-Encrypt"

### Assgin Root User Premises ###
if [ $UID != $? ]
then
 echo "Login Root User"
 exit 0
fi

### Folder Creation ###
if [ ! -d "$Destination" ]
then
   mkdir -p $Destination && chmod 700 $Destination
fi
find $Source -name "*" | grep 'tdr' > temp

### Encryting the Files ###
for FileList in `cat temp`
do
FName=`basename $FileList | awk -F"." '{print $1}'`
DName=`dirname $FileList | cut -b 11-`
if [ ! -d "$Destination/$DName" ]
then
   mkdir -p "$Destination/$DName" && chmod 700 "$Destination/$DName"
fi
cat $FileList | openssl enc -base64 > $Destination/$DName/$FName.ENC
chmod 500 $Destination/$DName/$FName.ENC
done

### Making Zip Files ####
cd $Destination
zip -r -e -P $SrcDir $SrcDir.zip $SrcDir/* > /dev/null
chmod 700 $SrcDir.zip
cd 
rm -rf $Destination/$SrcDir
rm -rf temp
