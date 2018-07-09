jq . test.log | egrep -i "eventti|eventsou|eventname|awsregi|creationdate" | tr -d '\n' | tr -s ' | uniq

ls | awk '{print"mv "$0" "$0}' | grep _04 | sed 's/_04/_40/2'

awk '{for (i=NF;i>0;i--) printf("%s ",$i)} {printf("%s","\n")}' $InFile

echo "00000006949873633_06.FMR" | rev

ls | head -n 1 | sed 's/_01/_05/g'

sed = sedr.txt | sed 'N;s/\n/\t/'

sed = emp.txt | sed 'N;s/\n/\. /' > emp1.txt

sed -n '$=' sedr.txt


sort -u kbc.txt -o tt.txt

for i in `cat list`; do cp "$i"  "$i".bak ; done

for counter in {1...5};do useradd user$counter;done

for user in `cat user.list`;do useradd $user;done

rsync -v -e ssh emp.txt  root@172.16.113.152:/opt

tac -s ' ' rev.txtsed '8,$ { $! s:</\?i>::g }'

dd if=/dev/zero of=/swap bs=1M count=1024
mkswap /swap

swapon /swap

date --date='2 days ago'

date --date='25 Dec' +%j

date '+%B %d'

date -s "2 OCT 2006 18:00:00"


date --set="2 OCT 2006 18:00:00"

date +%Y%m%d -s "20081128"


date +%T -s "10:13:13"

date +%T%p -s "6:10:30AM"

date +%T%p -s "12:10:30PM"


fuser -k 80/tcp


sed -e 's~,~~7' data7.txt 

sed '3 a\  u r my love' data7.txt

awk -v OFS='|' '{$1=$1};1' ts.txt

awk '{ print $1"|"$2"|"$3"|"$4"|"$5 }' ts.txt

cat biometric_photo_1105131308_05_508546_0001.FPP | cut -d "_" -f 4

for x in `cat gt.txt` do grep $x fg.txt >> asw.txt done


cp comp2.txt comp11.txt

for i in `cat comp1.txt` ;do grep -v $i comp11.txt > comp12.txt cp comp12.txt comp11.txt done

curl -IL "127.0.0.1:8080/jenkins

curl -IL "localhost:9090/DMaaP/dmaaprest/apiKeys"




count=0;while true;do;if [ $count -lt 10 ];then;let count++;status1=`curl -sI http://www.google.com|head -1`;
echo "loadtesting:$status1";else exit 0;fi;done


find test9/* -type f -exec chmod 777 {} ";"
find test9/* -type d -exec chmod 777 {} ";"



for i in *.TD2; do mv $i /root/kx/${i/_/}; done 

for i in `ls -1` ;do x=`echo $i |sed 's/_//1'` mv $i /<destination_path>/$x done 
 
echo "00202_19042013_99_16_508546.TD2" |awk -F'_' 'BEGIN{OFS="_";} {print $1$2,$3,$4,$5}' 
 
for i in *.TD2; do mv $i /root/kx/${i/_/}; done 

ls -ltr | awk '$6 == "Aug" {print"cp -rvf "$9" /tmp/"}'

cat test32 | sed 's/.$//g' | awk '{x+=1}{print$1" "$2x}' 


ls biometric_photo_28520131604_09_02477_12.FMR | awk -F"_" '{for(x=1;x<=9;x++) {print"cp -rvf " $0" "$1"_"$2"_"$3"_0"x"_"$5"_"$6}}' | sh 


cat td | egrep -o "[0-9\.]+" > td1 

cat fbtest.txt | awk '{print $1": "$2": "$3": "$4}' 

cat hips9 | awk '{print $0":385:root:redhat"}' > tg 
sed 's/$/:385:root:redhat/g' test 



'{if (substr($0,length($0)) % 2 == 1) print "#"$0; else print $0 }' ip1 > ip2 

echo RGB_DAILY_SNAPSHOT_20140926.txt | egrep -o "[[:digit:]]+"

echo "RGB_DAILY_SNAPSHOT_20140926.txt"|tr -d [A-Z][a-z][","] 

ps -ef | grep [t]ail | awk '{print $2}' | xargs -I {} kill {}

ls *csv | awk -F"." '{print"mv -v "$0" "$1".txt"}' | sh 
 
for file in (ls *.csv) ; do mv $file $(file%.csv).txt done 



10.135.2.16   www.abc.com www 
10.135.2.16   www.xyz.com www 
 
sed -e "\$a10.135.2.16 www.abc.com www \n10.135.2.16 www.xyz.com www" -i <filename>

sshpass -p root ssh -q   user@ip 'echo this is a test `hostname`'
sshpass -p iis123 ssh -q  user@ip 'hostname'
sshpass -p iis123 ssh -q  user@ip "hostname"
sshpass -p 'iis123' ssh -t user@ip -o StrictHostKeyChecking=no "date"

/bin/packer build --var-file credentials.json p.json
python -m easy_install -f http://math.uic.edu/t3m/plink plink







