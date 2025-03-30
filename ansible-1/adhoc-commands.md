

```

Ansible commands - 01
-----------------------

1. `ansible -i ec2.py -u ubuntu us-east-1d -m ping`
2. `ansible -i ec2.py -u deploy -m ping tag_app_1_my_dev`
3. `ansible-playbook -i ec2.py test.yml -e "variable_host=tag_app_1_my_dev user=deploy"`
4. `ansible -i aws_ec2.yml tag_aws_autoscaling_groupName_test_asg -m shell -a "df -k" -u ec2-user --private-key=plato_key.pem`
5. `ansible-playbook -i aws_ec2.yml docker_handler.yml -u ec2-user --private-key=plato_key.pem --extra-vars "nodes=tag_aws_autoscaling_groupName_test_asg"`
6. `ansible-playbook -i aws_ec2.yml docker_handler.yml -u ec2-user --private-key=plato_key.pem --extra-vars "nodes=ec2-3-87-0-103.compute-1.amazonaws.com"`
7. `ansible all --list-hosts`
8. `ansible-inventory --graph`
9. `ansible-inventory --list`
10. `ansible all -m ping`
11. `ansible-inventory --list -i aws_ec2.yml`
12. `ansible -i aws_ec2.yml -m ping all`
13. `ansible -i aws_ec2.yml tag_aws_autoscaling_groupName_test_asg -m shell -a "df -k" -u ec2-user –-private-key=plato_key.pem`
14. `ansible -i aws_ec2.yml tag_OS_UBUNTU14  -m authorized_key -a "user=ec2-user key='{{ lookup('file', '/root/.ssh/id_rsa.pub') }}'"`
15. `ansible -i aws_ec2.yml tag_OS_UBUNTU14 -m shell -a "apt-get install nginx" -u ec2-user –private-key=plato-key.pem`
16. `ansible -i aws_ec2.yml -m ping aws_ec2`
17. `ansible -i ec2.py tag_OS_UBUNTU14 -m ping -u ubuntu – private-key=<keyfilename.pem>`
18. `ansible -i ec2.py tag_OS_UBUNTU14 -m shell -a "df -k" -u ubuntu – private-key=<keyfilename.pem>`


Ansible commands - 02
-----------------------

1. `ansible-playbook test.yml  -v -vvvv -u deploy -i ec2.py`
2. `./ec2.py --host ec2-12-12-12-12.compute-1.amazonaws.com`
3. `ansible -i ec2.py -m ping tag_app_1_my_dev -u deploy`
4. `ansible -i ec2.py -u ubuntu us-east-1d -m ping`
5. `ansible -i ec2.py -u deploy -m ping tag_app_1_my_dev`
6. `ansible -i ./ec2.py --limit`
7. `ansible -i ec2.py --limit "tag_app-1_my-dev:&tag_app-2_my-dev-2" -m ping all`
8. `ansible -i ec2.py --limit "tag_app-1_my-dev" -m ping all`
9. `"tag_app-1_my-dev"`
10. `ansible -i ec2.py -u ubuntu us-east-1d -m ping`
11. `./ec2.py --list --profile default --refresh-cache`
12. `./ec2.py –list`
13. `ansible -i inventory/ec2.py -u ec2-user us-east-1a -m ping --key-file=vpn41.pem`
14. `ANSIBLE_PYTHON_INTERPRETER=auto_silent ansible -i inventory/ec2.py -u ec2-user us-east-1a -m ping --key-file=vpn41.pem`
15. `ANSIBLE_PYTHON_INTERPRETER=auto_silent ansible -i inventory/ec2.py -u ec2-user 44.199.209.84 -m ping --key-file=vpn41.pem`
16. `ANSIBLE_PYTHON_INTERPRETER=auto_silent ansible-playbook -i inventory/ec2.py -u ec2-user helo.yml --key-file=vpn41.pem --extra-vars "host=us-east-1a"`
17. `ansible-role nginx -i 192.168.10.27`
18. `ansible-playbook -i  "192.168.10.27" --tags "nginx"`
19. `ansible-playbook nginx-v.1.0.1.yml --extra-vars "variable_host=192.168.10.27"`
20. `ansible-playbook nginx-v.1.0.1.yml -i /etc/ansible/infra --extra-vars "host=web"`
21. `ansible-playbook release.yml --extra-vars "hosts=vipers user=starbuck"`
22. `ansible-playbook nginx-v.1.0.1.yml -i /etc/ansible/inventory --extra-vars "host=web user=deploy"`
23. `ansible-playbook nik-zoo.yml --extra-vars "host=web user=deploy"`
24. `ansible-playbook nik-zoo.yml --extra-vars "nodes=sandbox user=deploy"`
25. `ansible-playbook -i local-inventory.yml nik-zoo.yml --extra-vars "nodes=sandbox user=deploy"`
26. `ansible-role  --verbose --gather --extra-vars "variable_host=192.168.10.27" -i /etc/ansible/infra --hosts web --become yes --user deploy roles/nginx`
27. `date +"%m-%d-%y"`
28. `ansible-playbook play.yml -i hosts/dev/inventory --extra-vars "nodes=web user=deploy"`
29. `ansible-playbook nginx-v.1.0.1.yml -i hosts/dev/inventory --extra-vars "nodes=web user=deploy"`
30. `ansible-playbook test.yml -i ec2.py --extra-vars "user=deploy"`
31. `ansible-playbook test.yml  -v -vvvv -u deploy -i ec2.py`
32. `./ec2.py --host ec2-12-12-12-12.compute-1.amazonaws.com`
33. `ansible -i ec2.py -m ping tag_app_1_my_dev -u deploy`
34. `ansible -i ec2.py -u ubuntu us-east-1d -m ping`
35. `ansible -i ec2.py -u deploy -m ping tag_app_1_my_dev`
36. `ansible-playbook -i ec2.py test.yml -e "variable_host=tag_app_1_my_dev user=deploy"`
37. `ansible-playbook test-1.yml -i aws_inventory-root.yml --extra-vars "nodes=web" -vvvv`
38. `ansible-playbook test.yml -i aws-inventory-sudo.yml --extra-vars "nodes=web" -vvvv`
39. `ansible -i aws_inventory-root.yml -u root -m ping web`
40. `ansible -i aws_inventory-sudo.yml -u deploy -m ping web`
41. `ansible -i inventory/default/aws-inventory-sudo.yml -u deploy -m ping web`
42. `ansible-playbook play.yml -i aws_inventory-root.yml --extra-vars "nodes=web" -vvvv`
43. `ansible -i aws_inventory-root.yml -u root -m shell -a 'free -m' web123`
44. `ansible -i aws_inventory-sudo.yml -u deploy -m shell -a 'free -m' web123`
45. `ansible-playbook test.yml -i aws-inventory-sudo.yml --extra-vars "nodes=web" -vvvv`
46. `ansible-playbook playbooks/sc/test.yml -i inventory/default/aws-inventory-sudo.yml --extra-vars "nodes=qa"`
47. `ansible -i ./ec2.py --limit`
48. `ansible -i ec2.py --limit "tag_app-1_my-dev:&tag_app-2_my-dev-2" -m ping all`
49. `ansible -i ec2.py --limit "tag_app-1_my-dev" -m ping all`
50. `"tag_app-1_my-dev"`
51. `ansible -i ec2.py -u ubuntu us-east-1d -m ping`
52. `./ec2.py --list --profile default --refresh-cache`
53. `./ec2.py –list`
54. `ansible-inventory -i aws_ec2.yml --list`
55. `ansible -i aws_ec2.yml all -m ping -u ec2-user --key-file=ag-key.pem`
56. `ansible -i aws_ec2.yml all -m shell -a 'free -m' -u ec2-user --key-file=ag-key.pem`
57. `ansible -i aws_ec2.yml tag_Name_bastion_jenkins -m shell -a 'free -m' -u ec2-user --key-file=ag-key.pem`
58. `ansible-playbook -i aws_ec2.yml mem.yml -e "nodes=ec2-15-206-81-141.ap-south-1.compute.amazonaws.com user=ec2-user ansible_ssh_private_key_file=/home/nik/Desktop/ansible/aws-connect/ag-key.pem"`
59. `ansible-playbook -i aws_ec2.yml mem.yml -e "nodes=tag_Name_bastion_jenkins user=ec2-user ansible_ssh_private_key_file=/home/nik/Desktop/ansible/aws-connect/ag-key.pem"`
60. ansible-inventory -i aws_ec2.yaml --list

```

```
