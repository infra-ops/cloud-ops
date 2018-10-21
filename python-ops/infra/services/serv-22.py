#!/usr/bin/python
from time import strftime, localtime
import subprocess

log_data = []

def run_cmd(host,user,pwd, command):
        subprocess_command = ["sshpass", "-p", pwd, "ssh",\
                                '-q', "-o", "ConnectTimeout=5", "-o", "UserKnownHostsFile=/dev/null", "-o", "StrictHostKeyChecking=no",\
                                "{0}@{1}".format(user, host), command]

        p = subprocess.Popen(subprocess_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        (output, err) = p.communicate()

        if err == None or err == "":
                log_data.append("User creation successful on {0}".format(host))
                print log_data[-1]
        else:
                log_data.append("User creation unsuccessful on {0}".format(host))
                print log_data[-1]

if __name__ == '__main__':

        log_data.append("Script started at {0}".format(strftime("%d-%m-%Y-%H-%M-%S", localtime())))
        print log_data[-1]

        try:
                import sys
                args = sys.argv
                hosts = ""
                tasks = ""

                import yaml
                for i in range(len(args)):
                        if args[i] == '-h':
                                hosts = open(args[i+1], 'rb').read()
                        elif args[i] == '-t':
                                tasks = yaml.load(open(args[i+1], 'rb'))

                hosts = hosts.split('\n')

                for host in hosts:
                        if '[' in host:
                                pass
                        else:
                                host = host.replace('  ', ' ')
                                split = host.split(' ')

                                if len(split) <= 2 or '=' not in split[1] or '=' not in split[2]:
                                        continue

                                for task in tasks:
                                        for command in task['tasks']:
                                                run_cmd(split[0], split[1].split('=')[1], split[2].split('=')[1], command['user'])
        finally:
                log_data.append("Script finished at {0}".format(strftime("%d-%m-%Y-%H-%M-%S", localtime())))
                print log_data[-1]

                with open("status_" + strftime("%d-%m-%Y-%H-%M-%S", localtime()) + ".log", "wb") as log_file:
                        log_file.write("\n".join(log_data))
