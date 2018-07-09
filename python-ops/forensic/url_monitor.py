import requests
import datetime
target_url = "http://www.infibeam.com/new-release-books"
#resp = requests.get(target_url)
#print resp.status_code

current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

f_live = open("live_status_" + current_time_string  + ".txt" , "w") 

f_dead = open("dead_status_" + current_time_string  + ".txt", "w") 
    

url_list = ["http://www.google.com/", 
            "http://www.yahoo.com/", 
            "http://www.kskskskksks.com/"]

for url in url_list:
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            status = "%s is live\n" % ( url )
            f_live.write(status)
    except:
        status = "%s does not seem to be a real website" % ( url )
        f_dead.write(status)

f_live.close()
f_dead.close()    
