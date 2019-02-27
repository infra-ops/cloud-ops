#!/bin/bash

cmd()
{
cmd1=$(df -T);
cmd2=$(uptime);


echo "${cmd1}"
echo "${cmd2}"


}

cmd


