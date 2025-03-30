

```yaml
## Cron Use
---
- name: Set up a cron job
  hosts: your_hosts
  become: true
  tasks:
    - name: Add a cron job to run a script every day at 1 AM
      cron:
        name: "Run my script"
        minute: 0
        hour: 1
        job: "/path/to/your/script.sh"

```
