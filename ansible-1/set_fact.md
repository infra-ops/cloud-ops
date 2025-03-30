```

- name: Regex Playbook
  hosts: all
  vars:
    centos_repo: http://mirror.centos.org/centos/7/os/x86_64/Packages/
  tasks:
    - name: Get Latest Kernel
      uri:
        url: "{{ centos_repo }}"
        method: GET
        return_content: true
        body_format: json
      register: available_packages

    - name: Save
      set_fact:
        kernel: "{{ available_packages.content | ansible.builtin.regex_replace('<.*?>') | regex_findall('kernel-[0-9].*rpm') }}"

    - name: Print
      debug:
        var: kernel




- name: Get VPC Subnet ids which are available and public
    set_fact:
      vpc_subnet_id_public: "{{ subnet_facts_public.subnets|selectattr('state', 'equalto', 'available')|map(attribute='id')|list|random }}"
    when: region == "us-west-2"



---
- name: Example playbook with set_fact
  hosts: all
  tasks:
    - name: Set custom fact
      set_fact:
        my_custom_fact: "Hello, world!"

    - name: Print custom fact

```
      debug:
        msg: "The custom fact is {{ my_custom_fact }}"
