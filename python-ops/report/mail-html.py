import re
import subprocess
from email import Encoders
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


def mail():
         msg = MIMEMultipart()
	 msg["From"] = "neimer786@gmail.com"
	 msg["To"] = "neimer786@gmail.com"
	 msg["Subject"] = "Report Ansible."
         part = MIMEBase('application', "octet-stream")
         msgAlternative = MIMEMultipart('alternative')
         msg.attach(msgAlternative)
         msgText = MIMEText('Monitor Me')
         msgAlternative.attach(msgText)
	 htf = open("sample.html","rb")
         msgText = MIMEText(htf.read(), 'html')
	 htf.close()
         msg.attach(msgText)
       	 #part.set_payload(open("sample.csv", "rb").read())
	 Encoders.encode_base64(part)
         #part.add_header('Content-Disposition', 'attachment', filename="sample.csv")
        
         p =subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
	 p.communicate(msg.as_string())

mail()


