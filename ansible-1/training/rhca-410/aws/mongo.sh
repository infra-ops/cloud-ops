docker run --name dev-mongo  -p 27017:27017 -v /opt/apps/mongo-data:/data/db -d mongo

mongo 172.17.0.7:27017/inventory -u wadmin -p iis123
