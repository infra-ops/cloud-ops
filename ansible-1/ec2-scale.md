
Ec2 Autoscaling

[inventory]

enable_plugins = aws_ec2

inventory      = /opt/ansible/inventory/aws_ec2.yaml



ansible-inventory -i aws_ec2.yaml --list

ansible aws_region_us_west_2 -m ping

## Cat test.yml
```yaml
---
- name: Ansible Test Playbook
  gather_facts: false
  hosts: aws_region_us_east_1
  tasks:

    - name: Run Shell Command
      command: echo "Hello World"
```

# Ec2 Autoscaling
## Cat aws_ec2.yml

```yaml
---
plugin: aws_ec2
regions:
  - us-east-1
keyed_groups:
  - key: tags
    prefix: tag
```

```yaml
---
- hosts: sit
  tasks:
      - name: print hello
        shell: echo "hello world" 
        register: helo

      - name: Print helo
        debug:
          msg: "helo output: {{ helo.stdout }}"
```


```
cat aws_ec2.yaml 
---
plugin: aws_ec2
regions:
  - "us-east-1"keyed_groups:
  - key: tags.Name
  - key: tags.task
filters:
  instance-state-name : running
compose:
  ansible_host: public_ip_address



ansible.cfg

[defaults]
enable_plugins = aws_ec2
host_key_checking = False
pipelining = True
#remote_user = ec2-user
#private_key_file=/pem/key-pem
host_key_checking = False
inventory=inventory.txt
interpreter_python=auto_silent

ansible-inventory -i my_aws_ec2.yml --list

ansible-playbook update_env.yaml -i my_aws_ec2.yml --limit env_dev -vv

ansible -i ec2.py tag_ubuntu_tag_OS_UBUNTU14 -m shell -a "df -k" -u ubuntu --private-key=/home/nik/Desktop/keys/vpn41.pem

```

