#!/bin/bash

IP=( 'xxxxxxx' )
USER='xxxx'
PASS='xxxx'
SSH='sshpass -p '$PASS' ssh -n -o StrictHostKeyChecking=no'
CMD1='/opt/dev/n.sh'
CMD2='/opt/dev/k.sh'

SOURCE='/home/nik/script/*.sh'
DEST='/opt/dev'

   for IPS in "${IP[@]}"
   do
    sshpass -p $PASS scp   -r  $SOURCE  $USER@$IPS:$DEST
    $SSH    $USER@$IPS "bash ${CMD1} ; bash ${CMD2}"
     done
