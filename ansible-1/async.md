
```yaml
##Async Usage
---------------

- hosts: all
  tasks:
    - name: Run a long-running command asynchronously
      shell: /path/to/long_running_script.sh
      async: 3600  # Run the task asynchronously for up to 1 hour
      poll: 0  # Disable polling for completion

    - name: Wait for the asynchronous task to complete
      async_status:
        jid: "{{ ansible_job_id }}"  # Use the job ID from the asynchronous task
      register: job_result
      until: job_result.finished
      retries: 360  # Poll the status every 10 seconds for up to 1 hour
      delay: 10  # Wait 10 seconds between retries

```
