"""
{
"code":"S25"
"trigger": "email"
}
"""


import json
import jwt
import re
import subprocess
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from email import Encoders
from email.MIMEBase import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from tornado.options import define, options



#Kindly click on below mentioned url to check patch updates
#     http://ec2-54-159-8-36.compute-1.amazonaws.com/patch/
def mail():
         msg = MIMEMultipart()
         msg["From"] = "me@example.com"
         msg["To"] = "sudipta1436@gmail.com"
         msg["Subject"] = "Report Ansible."
         text="""Kindly click on below mentioned url to check patch updates\nhttp://ec2-54-159-8-36.compute-1.amazonaws.com/patch/"""
         msg.attach(MIMEText(text))
         p =subprocess.Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=subprocess.PIPE)
         p.communicate(msg.as_string())

define("port", default=8000, help="run in the given port", type=int)

auth=[]
algh="HS256"


encoded=jwt.encode({"message":"email delivered"}, 'secret', algorithm=algh)

class AuthHandler(tornado.web.RequestHandler):
    def post(self):
        auth.append(json.loads(self.request.body))
        if (auth[0]["code"] == algh):
            data=jwt.decode(encoded, 'secret', algorithms=[algh])
            mail()
            self.write(data)
            auth[0]["code"]=""
        else:
            self.write({"message": "Not Allowed"})

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app=tornado.web.Application(handlers=[(r"/auth", AuthHandler)])
    http_server=tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
