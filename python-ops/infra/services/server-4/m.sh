sync; echo 3 > /proc/sys/vm/drop_caches

free -m

#free -m | sed -n -e '3p' | grep -Po "\d+$"


#watch -n 1 free -m
