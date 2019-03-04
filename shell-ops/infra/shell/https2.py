WORKDIR="/root/shell/port"
HTTPSSERVERIP="172.16.188.167"
HTTPSSERVERPORT="5000"
EMAIL=chakraborty.rock@gmail.com

### Binaries ###
MAIL=$(which mail)
TELNET=$(which telnet)
DIG=$(which dig)
###Change dir###
#cd $WORKDIR

###Test HTTPS###


(
echo "quit"
) | $TELNET $HTTPSSERVERIP $HTTPSSERVERPORT | grep Connected > /dev/null 2>&1
if [ "$?" -ne "1" ]; then #Ok
echo "PORT CONNECTED"
if [ -f server_problem_first_time_https.txt ]; then #remove file if problem fixed
rm -rf server_problem_first_time_https.txt
fi
else #Connection failure
if [ -f server_problem_first_time_https.txt ]; then #Second time, send notification below
echo "HTTPS PORT NOT CONNECTING" >> server_problem.txt
rm -rf server_problem_first_time_https.txt
else #First notification
    > server_problem_first_time_https.txt
fi
fi


###Send mail notification after 2 failed check###
if [ -f server_problem.txt ]; then
#$MAIL -s "Server problem" $EMAIL <  server_problem.txt
 mailx -s "Server problem" -r  no-reply@ril.com chakraborty.rock@gmail.com < server_problem.txt

fi

