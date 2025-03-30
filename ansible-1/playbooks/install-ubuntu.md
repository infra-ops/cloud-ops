```
---
- name: Upgrade vim, nginx, and kernel to specific versions (Ubuntu)
  hosts: all
  become: yes
  vars:
    kernel_version: "5.15.0-91-generic"

  tasks:
    - name: Upgrade vim and nginx to specific versions
      apt:
        name: "{{ item.name }}={{ item.version }}"
        state: present
      loop:
        - { name: vim, version: "8.2.3437" }
        - { name: nginx, version: "1.22.1" }
      tags: [upgrade, packages]

    - name: Ensure APT cache is updated
      apt:
        update_cache: yes
      tags: [upgrade]

    - name: Install specific kernel version
      apt:
        name: "linux-image-{{ kernel_version }}"
        state: present
      tags: [upgrade, kernel]

    - name: Check if current kernel matches the target version
      shell: "uname -r"
      register: current_kernel
      changed_when: false
      tags: [verify]

    - name: Reboot system if kernel not active
      reboot:
        reboot_timeout: 300
      when: current_kernel.stdout != kernel_version
      async: 1
      poll: 0
      tags: [kernel, reboot]

    - name: Wait for system to become reachable
      wait_for_connection:
        timeout: 300
      when: current_kernel.stdout != kernel_version
      tags: [kernel, reboot]

    - name: Verify new kernel version after reboot
      shell: "uname -r"
      register: new_kernel
      changed_when: false
      tags: [verify]

    - name: Verify vim and nginx versions
      shell: "dpkg -l {{ item.name }} | grep {{ item.name }}"
      loop:
        - { name: vim }
        - { name: nginx }
      register: apt_list_check
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

    - name: Debug APT output
      debug:
        msg: "APT List Output: {{ item.stdout }}"
      with_items: "{{ apt_list_check.results }}"
      tags: [verify]

    - name: Debug vim version
      debug:
        msg: "Vim Version: {{ vim_version_check.stdout }}"
      tags: [verify]

    - name: Debug nginx version
      debug:
        msg: "Nginx Version: {{ nginx_version_check.stdout }}"
      tags: [verify]

    - name: Debug current kernel after reboot
      debug:
        msg: "Kernel Version: {{ new_kernel.stdout }}"
      tags: [verify]

```
