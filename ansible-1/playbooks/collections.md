
Collection
-------------

```

mkdir -p /ansible_collections/

cd /ansible_collections/

ansible-galaxy collection init nik786.blue

cd /ansible_collections/nik786/blue

ansible-galaxy role init roles/blue-app

cat roles/blue-app/tasks/main.yml 
---

- name: Hello world from Ansible collection
  debug:
    msg: "Hello, Ansible Galaxy!"


ansible-galaxy collection build

ansible-galaxy collection publish nik786-blue-1.0.0.tar.gz --api-key 5279c59


Create an account on https://galaxy.ansible.com/

Link it to your GitHub namespace

Create an API token under your profile (My Content → API tokens)



```
