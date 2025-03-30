


```
- synchronize:
   src: /first/absolute/path
   dest: /second/absolute/path
   delegate_to: "{{ inventory_hostname }}"

- copy:
   src: /first/absolute/path
   dest: /second/absolute/path


- name: Unarchive a file that is already on the remote machine
  ansible.builtin.unarchive:
    src: /tmp/foo.zip
    dest: /usr/local/bin
    remote_src: yes


- name: Create a JIRA issue
  uri:
    url: https://your.jira.example.com/rest/api/2/issue/
    user: your_username
    password: your_pass
    method: POST
    body: "{{ lookup('ansible.builtin.file','issue.json') }}"
    force_basic_auth: true
    status_code: 201
    body_format: json


- name: Download a file using get_url
  get_url:
    url: https://example.com/file.tar.gz
    dest: /tmp/file.tar.gz

```


```
