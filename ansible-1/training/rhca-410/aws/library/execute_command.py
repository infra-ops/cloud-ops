#!/usr/bin/python
import subprocess
DOCUMENTATION = '''
module: execute_command
short_description: "Executes the issued command and prints the output of the command"
author:
  - your name
requirements:
  - only standard library needed
options:
  command:
    description:
      - the command you wanted to execute on the node.
      required: true
      default: null
example:  execute_command: command=ls
'''
def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    result,error_msg = process.communicate()
    if result:
        return True, result
    else:
        return False, error_msg
def main():
    # The AnsibleModule provides lots of common code for handling returns, parses your arguments for you, and allows you to check inputs
    module = AnsibleModule(
        argument_spec=dict(
            command=dict(required=True)
        ),
        supports_check_mode=True
    )
    # in check mode we take no action
    # since this module actually never changes system state we'll just return False
    if module.check_mode:
        module.exit_json(changed=False)
    command = module.params['command']
    status, result  = execute_command(command)
    if status:
        print result
        module.exit_json(changed=True,result=result)
    else:
        msg = "Command %s is failed on this host" % (command)
        module.fail_json(msg=result)
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
