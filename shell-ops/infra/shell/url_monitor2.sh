lynx -dump $1 &> /dev/null
if [ $? = 0 ]
then
echo “website is up”
else
echo “website is down. Trigger the email”
fi

Output :

$ ./website_test.sh http://google.com
website is up
$ ./website_test.sh http://google32323232.com
