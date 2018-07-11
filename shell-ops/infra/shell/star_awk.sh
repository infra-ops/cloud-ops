#!/bin/sh
awk 'BEGIN (i<6)
{i++ $i=OFS="*" print $i=""}}'
