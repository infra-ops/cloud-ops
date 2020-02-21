import yaml
import paramiko
import boto3
import re
import getopt
import sys
import smtplib
from datetime import datetime
from email.mime.text import MIMEText




def check_result_from_service_command(a):
    if isinstance(a, list):
        a = ''.join(a)

    ok = re.findall(r"(is running|ok)", a, re.IGNORECASE)
    if ok:
        return True
    else:
        return False


def check_result_from_other_command(a):
    if isinstance(a, list):
        a = ''.join(a)
    if len(a) > 0:
        return True
    else:
        return False

def get_execute_commands(file_config):
    f = open(file_config, 'r')
    docs = yaml.load_all(f)
    available_cmds = []
    for doc in docs:
        for i in doc.get('tasks'):
            available_cmds.append(i)
    f.close()
    return available_cmds

def get_servers(file_config, cmds, log):
    # initialize ssh
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    pre_command = """export PATH=$PATH:/sbin; """

    f = open(file_config, 'r')
    docs = yaml.load_all(f)

    for doc in docs:
        for region in doc:
            print region
            for server in doc.get(region):
                print server
                username = str(server['user'])
                password = str(server['pass'])
                hostname = str(server['host'])
                # try:
                ssh.connect(hostname, username=username, password=password)
                # except:
                #     continue

                # run each command
                for cmd in cmds:
                    if cmd['host'] != server['host']:
                        continue
                    cmd_to_execute = pre_command + cmd['cmd']
                    cmd_name = cmd['name']
                    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd_to_execute)
                    if cmd['cmd'].startswith('service'):
                        result = check_result_from_service_command(ssh_stdout.readlines())
                    else:
                        result = check_result_from_other_command(ssh_stdout.readlines())

                    # if result good
                    if result:
                        log.write('{0} - OK - {1}\n'.format(cmd_name, hostname))
                    else:
                        log.write('{0} - NOT OK - {1}\n'.format(cmd_name, hostname))

def email(logfile):
    with open(logfile, 'rb') as f:
        msg = MIMEText(f.read())
        msg['Subject'] = 'Kindly check status of service in attachment'
        msg['From'] = 'checkserver@alert.com'
        msg['To'] = 'kenvin.md@gmail.com'
        s = smtplib.SMTP('localhost')
        s.sendmail(msg['From'], msg['To'], msg.as_string())
        s.quit()

def public_to_sns(logfile):
    with open(logfile, 'rb') as f:
        client = boto3.client('sns')
        response = client.publish(
            TopicArn='<your topic arn>',
            Message=f.read()
        )

def main():
    f = open('logfile.txt','w')
    S3_BUCKET = ''

    # read from commandline
    opts, args = getopt.getopt(sys.argv[1:], "n:s:b:")
    file_status = 'status.yml'
    file_node = 'node.yml'
    for o, a in opts:
        if o == '-n':
            file_node = a
        elif o == '-s':
            file_status = a
        elif o == '-b':
            S3_BUCKET = a

    # avaiable command
    cmds = get_execute_commands(file_status)
    get_servers(file_node, cmds, f)
    f.close()

    # put log to S3
    # client = boto3.client('s3')
    s3 = boto3.resource('s3')
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + '.log'
    s3.meta.client.upload_file('logfile.txt', S3_BUCKET, filename)

    # send email attach log file
    # email('logfile.txt')
    public_to_sns('logfile.txt')


if __name__ == '__main__':
    main()
