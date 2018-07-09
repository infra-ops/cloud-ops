#!/bin/bash

echo >> tt
#echo "redirecting output of id"
/var/lib/jenkins/bin/terraform output id > tt
cat tt
