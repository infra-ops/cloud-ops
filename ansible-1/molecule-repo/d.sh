docker build -t jenkins/test-jen-2 .


docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
docker images
docker rmi $(docker images -q)
docker images



docker run --name jen1  -d -p 8080:8080 jenkins/test-jen-2

docker ps -a
docker exec -it 22b7ea5143dd /bin/bash -c "ps -ef | grep jenkins"
docker exec -it 22b7ea5143dd /bin/bash -c "cat /var/lib/jenkins/secrets/initialAdminPassword"


