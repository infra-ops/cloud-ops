

```

---
- name: Upgrade vim, nginx, and kernel to specific versions (RedHat)
  hosts: all
  become: yes
  vars:
    kernel_version: "4.18.0-477.19.1.el8_4"

  tasks:
    - name: Ensure YUM repository is up to date
      yum:
        name: '*'
        state: latest
        update_cache: yes

    - name: Upgrade vim and nginx to specific versions
      yum:
        name: "{{ item.name }}-{{ item.version }}"
        state: present
      loop:
        - { name: vim, version: "8.2.3437" }
        - { name: nginx, version: "1.22.1" }
      tags: [upgrade, packages]

    - name: Update kernel to a specific version
      yum:
        name: "kernel-{{ kernel_version }}"
        state: present
      tags: [upgrade, kernel]

    - name: Reboot system if kernel is updated
      shell: "uname -r | grep {{ kernel_version }}"
      register: kernel_check
      failed_when: kernel_check.rc not in [0, 1]
      changed_when: kernel_check.rc == 1
      notify: reboot
      tags: [kernel, verify]

    - name: Verify vim and nginx versions
      shell: "yum list installed {{ item.name }} | grep {{ item.name }}"
      loop:
        - { name: vim }
        - { name: nginx }
      register: yum_list_check
      changed_when: false
      tags: [verify]

    - name: Verify vim version
      shell: "vim --version | head -n 1"
      register: vim_version_check
      changed_when: false
      tags: [verify]

    - name: Verify nginx version
      shell: "nginx -v 2>&1"
      register: nginx_version_check
      changed_when: false
      tags: [verify]

    - name: Verify kernel version
      shell: "uname -r"
      register: kernel_version_check
      changed_when: false
      tags: [verify]

    - name: Debug YUM output
      debug:
        msg: "YUM List Output: {{ item.stdout }}"
      with_items: "{{ yum_list_check.results }}"
      tags: [verify]

    - name: Debug vim version
      debug:
        msg: "Vim Version: {{ vim_version_check.stdout }}"
      tags: [verify]

    - name: Debug nginx version
      debug:
        msg: "Nginx Version: {{ nginx_version_check.stdout }}"
      tags: [verify]

    - name: Debug kernel version
      debug:
        msg: "Kernel Version: {{ kernel_version_check.stdout }}"
      tags: [verify]

  handlers:
    - name: reboot
      command: /sbin/reboot
      async: 1
      poll: 0





ansible-playbook upgrade_vim_nginx_kernel.yml --tags "upgrade,verify"
ansible-playbook upgrade_vim_nginx_kernel.yml --skip-tags kernel

ansible-playbook upgrade_vim_nginx_kernel.yml --tags verify
ansible-playbook upgrade_vim_nginx_kernel.yml --skip-tags kernel



```
