function wait() {
local msg1=$1
local msg2=$2
local msg3=$3
            echo -e "\n\033[0m$1 $2 \t\t\t\t""[ \e[00;32m$3\e[00m ]"
sleep 1
}
IPLIST='pox'
#read -p "Enter the Name of IP list file with absolute path : " IPLIST
                if [ ! -f $IPLIST ];then
                echo ""
                echo "Please check the IPLIST file"
                exit 1
                fi
IP_LIST=`cat $IPLIST`
echo -e "\t\t\t\033[0m\e[0;1;4;100;36mCHECKING SERVER ACCESSABILITY FOR THE GIVEN IP LIST\e[00m"
for IP in $IP_LIST ;do
                ping -c 3 $IP 2> /dev/null 1> /dev/null
                        if [ $? == 0 ];then
                        wait "Pinging Server" "$IP" "SUCCESSFULL"
                        else
                        wait "Pinging Server" "$IP" "UNAVAILABLE"
                        fi
        done
echo -e "\n\033[0m\t\t\t\t\e[00;34;47m END OF THE SCRIPT \e[00m\n\n"

