docker run -d --name dev-mongo  -p 27017:27017 -v /opt/apps/mongo-data:/data/db \
    -e MONGO_INITDB_ROOT_USERNAME=mdmin \
    -e MONGO_INITDB_ROOT_PASSWORD=mpass \
    mongo

