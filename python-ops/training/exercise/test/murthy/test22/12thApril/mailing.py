from mailing_environment import *
import smtplib
import email
import os
from email.mime.text import MIMEText
from email import encoders 

# Mailing Demo
# Send a simple Text Email

FROM = "chakrabortyrock@gmail.com"
TO  = "murthyraju@gmail.com"
CC = "murthy.raju@gmail.com"
BCC = "murthy.r.aju@gmail.com"

ATTACHMENT_FILE_PATH = "/home/trainer/Desktop/logo.jpg"

SUBJECT = "Testing Mail Sending Using Python"
"""
server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
server.ehlo()
server.starttls()
#server.ehlo()
server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)

msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n" % (FROM, TO, SUBJECT)
msg += "This is a plain text mail to test \nsending mail from python.\n\nThanks\nMurthy Raju"

server.sendmail(FROM, TO, msg)
server.quit()

"""
# Sending a mail with attachment

msg = email.mime.Multipart.MIMEMultipart()

msg['Subject'] = SUBJECT  + " With Attachment"
msg['From'] = FROM
msg['To'] =  TO
msg['CC'] = CC
msg['BCC'] = BCC
   
body = MIMEText("This is a test mail with attachments. This is the plain text body")
msg.attach(body)

fp=open(ATTACHMENT_FILE_PATH,'rb')
attachment = email.mime.Multipart.MIMEBase('application', 'octet-stream')
attachment.set_payload(fp.read())

encoders.encode_base64(attachment)

fileName = os.path.basename(ATTACHMENT_FILE_PATH)
fileName = "New_logo_I_created.jpg"

attachment.add_header('Content-Disposition', 'attachment', filename=fileName)    

msg.attach(attachment)
fp.close()

service= smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
service.ehlo()
service.starttls()
#service.ehlo()
service.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)        

recipientList = []
recipientList.append(TO)
recipientList.append(CC)
recipientList.append(BCC)

service.sendmail(FROM, recipientList, msg.as_string())
service.quit()
