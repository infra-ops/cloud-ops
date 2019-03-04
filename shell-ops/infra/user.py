 user=nik20;u=$(grep -i "$user" /etc/passwd | cut -d ":" -f1) ; if [ "$user" == "$u" ] ;then echo "user does exist"; exit 2; else echo "creation of $user is ok"; useradd -m $user; fi
