import datetime

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

f1 = open('url-1' , 'r')
f2 = open("status" + current_time_string + ".txt" , 'w')



#curl -sI http://www.google.com|head -1`;
curl -SI $1  | head -1




echo "loadtesting:$status1"




f2.write()

f1.close()
f2.close()
f3.close()
