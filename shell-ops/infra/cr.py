for user in `cat users.txt`
do
crontab -u $user -l > /dev/null
if [ $? = 0 ]; then
echo $user >> cron_users.txt
else
echo $user >> non_cron_users.txt
fi
done
