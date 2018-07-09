docker run --name mongo-1  -d -p 27017:27107 -v /var/mongo:/data/db mongo
docker exec -it mongo-1 mongo admin
db.createUser({ user: 'xxx', pwd: 'xxxx', roles: [ { role: "userAdminAnyDatabase", db: "admin" } ] });
db.getName();
use teradb
db.node1.insert({"name":"10.0.2.5"})
show dbs
db.createCollection("nodedetails")
db.node2.insert({"name" : "10.0.2.7"})
db.node1.find().pretty()

db.nodestack.insert({_id: ObjectId(7df78ad8902c),ip: '10.0.2.5',pingable: 'no',ssh: 'yes'})
