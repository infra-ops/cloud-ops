from tornado import httpserver
from tornado import gen
from tornado.ioloop import IOLoop
import tornado.web
import json
from elasticsearch import Elasticsearch
import requests

i = 1

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('Send the JSON through POST method.')
    def post(self):
        body = json.loads(self.request.body.decode('utf-8'))
        #body[""] = ""
        #print "JSON Body: " + str(body)
        response = self.sendJSONtoElasticSearch(body, "localhost", 9200)
        self.write({"message": response})
    def sendJSONtoElasticSearch(self, json, host, port):
        es = Elasticsearch([{"host": host, "port": port}])
        r = requests.get("http://" + host + ":" +str(port) + "/")
        global i

        if r.status_code == 200:
            response = es.index(index="test_index", doc_type="log", body=json)
            i = i + 1
            return response
        else:
            return "Error, the Elasticsearch isn't running."

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/?", MainHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

def main():
    app = Application()
    app.listen(85)
    IOLoop.instance().start()

if __name__ == '__main__':
    main()
