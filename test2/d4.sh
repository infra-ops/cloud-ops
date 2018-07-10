
docker ps -a
docker exec -it 22b7ea5143dd /bin/bash -c "ps -ef | grep jenkins"
docker exec -it 22b7ea5143dd /bin/bash -c "cat /var/lib/jenkins/secrets/initialAdminPassword"


