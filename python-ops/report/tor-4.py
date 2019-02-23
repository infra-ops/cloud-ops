#!/usr/bin/env python3

import json
import jwt
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

define("port", default=8000, help="run in the given port", type=int)

auth=[]
algh="HS256"


encoded=jwt.encode({"user":"payload"}, 'secret', algorithm=algh)

class AuthHandler(tornado.web.RequestHandler):
    def post(self):
        auth.append(json.loads(self.request.body))
        if (auth[0]["code"] == algh):
            data=jwt.decode(encoded, 'secret', algorithms=[algh])
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
