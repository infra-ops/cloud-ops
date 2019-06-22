ansible -i ./ec2.py -m ping tag_ubuntu_dev_1_ubuntu_node_1 -u ubuntu


ansible -i ./ec2.py all -m ping -u deploy

ansible -i ./ec2.py all -m shell -a 'uptime'  -u deploy


mongoimport -h 127.0.0.1  --port 27017 --db inventory --collection nodes -u aws-admin -p iis123 --type json --file sample.json

mongoimport -h 172.17.0.7  --port 27017 --db inventory --collection localnodes -u wadmin -p iis123 --type json --file  sample.json

ansible -i ./inv.sh dev -m debug -a "msg={host_var}}"

ansible -m  setup -i remote.yml dev

ssh deploy@18.209.228.253

curl -s -u admin:password http://127.0.0.1/api/v2/hosts/ | python -m json.tool

curl -s -u admin:password http://127.0.0.1/api/v2/hosts/

ansible_facts.ansible_architecture:x86_64
