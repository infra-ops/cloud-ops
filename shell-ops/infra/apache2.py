p=`ps -ef | pgrep apache2 | wc -l`
if [-z "$p"]
then
echo "critical"
exit 2
else
if ["$p" -le "5"]
then
echo "warning"
exit 1
else
echo "no of running apache:""$p";
exit 0
fi
fi
