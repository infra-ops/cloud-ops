from flask import Flask, render_template, url_for, request
from cassandra.cluster import Cluster
from cqlengine.management import sync_table

app = Flask(__name__)

cluster = Cluster()
session = cluster.connect('rjil')

result = session.execute("select * from serverhall2")

@app.route("/")
def index():
    return render_template('index.html', result=result)

@app.route("/add/")
def add():
    return render_template('add.html')

@app.route("/addprocess/", methods=['POST'])
def addprocess():
    SERVERID = request.form['SERVERID']
    IP = request.form['IP']
    PINGABLE = request.form['PINGABLE']
    OSTYPE = request.form['OSTYPE']
    USERNAME = request.form['USERNAME']
    SUDO = request.form['SUDO']
    cluster = Cluster()
    session = cluster.connect('rjil')
    result = session.execute("INSERT INTO SERVERHALL2 (SERVERID, IP, PINGABLE,OSTYPE,USERNAME,SUDO) \
                VALUES (%s,%s,%s,%s,%s,%s)", (SERVERID, IP, PINGABLE,OSTYPE,USERNAME,SUDO, ))
    return 'data added'

if __name__ == "__main__":
    app.run()
