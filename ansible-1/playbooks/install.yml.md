

```

---
- name: Upgrade vim, nginx, and kernel to specific versions
  hosts: all
  become: yes
  tasks:
    # Upgrade vim and nginx to specific versions for RedHat-based OS
    - name: Ensure YUM repository is up to date (RedHat)
      yum:
        name: '*'
        state: latest
        update_cache: yes
      when: ansible_facts.os_family == "RedHat"

    - name: Upgrade vim and nginx to specific versions for RedHat
      yum:
        name: "{{ item.name }}-{{ item.version }}"
        state: present
      loop:
        - { name: vim, version: "8.2.3437" }
        - { name: nginx, version: "1.22.1" }
      tags:
        - upgrade
        - packages
      when: ansible_facts.os_family == "RedHat"

    - name: Upgrade vim and nginx to specific versions for Ubuntu
      apt:
        name: "{{ item.name }}={{ item.version }}"
        state: present
      loop:
        - { name: vim, version: "8.2.3437" }
        - { name: nginx, version: "1.22.1" }
      tags:
        - upgrade
        - packages
      when: ansible_facts.os_family == "Debian"

    # Update the kernel to a specific version only for RedHat-based OS
    - name: Update kernel to a specific version (RedHat)
      yum:
        name: "kernel-{{ kernel_version }}"
        state: present
      vars:
        kernel_version: "4.18.0-477.19.1.el8_4"
      tags:
        - upgrade
        - kernel
      when: ansible_facts.os_family == "RedHat"

    # Ensure the system uses the updated kernel only for RedHat-based OS
    - name: Reboot system if kernel is updated (RedHat)
      shell: "grubby --default-kernel | grep {{ kernel_version }}"
      register: grubby_check
      failed_when: grubby_check.rc not in [0, 1]
      changed_when: grubby_check.rc == 1
      notify:
        - reboot
      tags:
        - kernel
        - verify
      when: ansible_facts.os_family == "RedHat"

    # Verify package versions for RedHat-based OS
    - name: Verify vim and nginx versions using yum list installed (RedHat)
      shell: "yum list installed {{ item.name }} | grep {{ item.name }}"
      loop:
        - { name: vim }
        - { name: nginx }
      register: yum_list_check
      tags:
        - verify
      changed_when: false
      when: ansible_facts.os_family == "RedHat"

    # Verify vim version using vim --version for RedHat-based OS
    - name: Verify vim version using vim --version (RedHat)
      shell: "vim --version | head -n 1"
      register: vim_version_check
      tags:
        - verify
      changed_when: false
      when: ansible_facts.os_family == "RedHat"

    # Verify nginx version using nginx -v for RedHat-based OS
    - name: Verify nginx version using nginx -v (RedHat)
      shell: "nginx -v 2>&1"
      register: nginx_version_check
      tags:
        - verify
      changed_when: false
      when: ansible_facts.os_family == "RedHat"

    # Verify kernel version for RedHat-based OS
    - name: Verify kernel version using uname -r (RedHat)
      shell: "uname -r"
      register: kernel_version_check
      tags:
        - verify
      changed_when: false
      when: ansible_facts.os_family == "RedHat"

    # For Ubuntu, we can verify nginx and vim versions
    - name: Verify vim and nginx versions (Ubuntu)
      shell: "dpkg -l {{ item.name }} | grep {{ item.name }}"
      loop:
        - { name: vim }
        - { name: nginx }
      register: apt_list_check
      tags:
        - verify
      changed_when: false
      when: ansible_facts.os_family == "Debian"

    # Verify vim version using vim --version for Ubuntu
    - name: Verify vim version using vim --version (Ubuntu)
      shell: "vim --version | head -n 1"
      register: vim_version_check_ubuntu
      tags:
        - verify
      changed_when: false
      when: ansible_facts.os_family == "Debian"

    # Verify nginx version using nginx -v for Ubuntu
    - name: Verify nginx version using nginx -v (Ubuntu)
      shell: "nginx -v 2>&1"
      register: nginx_version_check_ubuntu
      tags:
        - verify
      changed_when: false
      when: ansible_facts.os_family == "Debian"

    # Debug outputs for all verification checks
    - name: Debug yum list output (RedHat)
      debug:
        msg: "YUM List Output: {{ item.stdout }}"
      with_items: "{{ yum_list_check.results }}"
      tags:
        - verify
      when: ansible_facts.os_family == "RedHat"

    - name: Debug apt list output (Ubuntu)
      debug:
        msg: "APT List Output: {{ item.stdout }}"
      with_items: "{{ apt_list_check.results }}"
      tags:
        - verify
      when: ansible_facts.os_family == "Debian"

    - name: Debug vim version output (RedHat)
      debug:
        msg: "Vim Version: {{ vim_version_check.stdout }}"
      tags:
        - verify
      when: ansible_facts.os_family == "RedHat"

    - name: Debug vim version output (Ubuntu)
      debug:
        msg: "Vim Version (Ubuntu): {{ vim_version_check_ubuntu.stdout }}"
      tags:
        - verify
      when: ansible_facts.os_family == "Debian"

    - name: Debug nginx version output (RedHat)
      debug:
        msg: "Nginx Version: {{ nginx_version_check.stdout }}"
      tags:
        - verify
      when: ansible_facts.os_family == "RedHat"

    - name: Debug nginx version output (Ubuntu)
      debug:
        msg: "Nginx Version (Ubuntu): {{ nginx_version_check_ubuntu.stdout }}"
      tags:
        - verify
      when: ansible_facts.os_family == "Debian"

    - name: Debug kernel version output (RedHat)
      debug:
        msg: "Kernel Version: {{ kernel_version_check.stdout }}"
      tags:
        - verify
      when: ansible_facts.os_family == "RedHat"

  handlers:
    - name: reboot
      command: /sbin/reboot
      async: 1
      poll: 0
      when: ansible_facts.os_family == "RedHat"



ansible-playbook upgrade_vim_nginx_kernel.yml --tags "upgrade,verify"
ansible-playbook upgrade_vim_nginx_kernel.yml --skip-tags kernel

ansible-playbook upgrade_vim_nginx_kernel.yml --tags verify
ansible-playbook upgrade_vim_nginx_kernel.yml --skip-tags kernel



```
