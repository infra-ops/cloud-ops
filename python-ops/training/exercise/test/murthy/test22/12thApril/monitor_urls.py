import requests
import datetime
import smtplib

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'chakrabortyrock@gmail.com'
EMAIL_HOST_PASSWORD = 'P@$$_w0rd'
EMAIL_PORT = 587

def send_mail(from_address, to_address, subject, body):

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (from_address, to_address, subject)
    msg += body

    server.sendmail(FROM, TO, msg)
    server.quit()
    
    print "Done sending mail to " + to_address    
    return True

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

    FROM = "chakrabortyrock@gmail.com"
    TO  = "murthyraju@gmail.com"
    SUBJECT = "Server is Dead. URGENT - " + url
    body = "Hi\nServer %s is dead. do something about it urgently.\n\nMonitoring Team" % (url,)

    send_mail(FROM, TO, SUBJECT, body)

    f_dead.write(status)

f_live.close()
f_dead.close()    
