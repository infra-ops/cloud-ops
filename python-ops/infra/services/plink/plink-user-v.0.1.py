import argparse
import datetime
import os
import re
import smtplib
import subprocess
import sys
import yaml
import boto3
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart



def error(msg, exit_code=-1):
    print("ERROR: %s" % msg)
    sys.exit(exit_code)


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
    available_cmds = []
    with open(file_config) as f:
        for _, node in yaml.load_all(f):
            for node in node.get('tasks'):
                available_cmds.append(cmd)
    return available_cmds




def test_plink():
    p = subprocess.Popen(["plink", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.wait() != 0:
        error("missing plink or plink wrongly installed on your system")


def plink(data):
    host, user, pwd = data['host'], data['user'], data['pass']
    remote_call = data['cmd-1']

    debug_call = "plink %s@%s -pwd %s \"%s\"" % (user, host, pwd, remote_call)
    #print("DEBUG: execute pink: %s" % debug_call)

    out = None
    p = subprocess.Popen(["plink",
        "%s@%s" % (user, host), "-pw", pwd, remote_call],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.wait() != 0:
        print("ERROR: plink returned with following error:\n %s" % p.stderr.read())
    else:
        out = p.stdout.read()
        print(out)
    return out


def is_result_valid(line):
    if line.count(",") != 4:
        print("ERROR: plink result format '%s' missmatched - can not be analyzed" % line)
        return False
    server_ip, exc_date, exc_time, value, perc = line.split(",")
    try:
        perc = int(perc)
    except:
        print("ERROR: plink 'percentage' result '%s' can not parsed" % perc)
        return False
    return perc <= 90


def main():
    """ Main method used from commandline."""
    # Test plink is installed on client
    test_plink()

    # Parsing commandline arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', help='config file (yaml)', metavar='CFG_YAML')
    
    args = parser.parse_args()

    # Validating parameters
    config_file = args.n
    if not os.path.isfile(config_file):
        error("config file '%s' does not exists" % config_file)

    # Process nodes with host lists configured within yaml file ...
    plink_results = []
    log_status = "ok"
    with open(config_file) as c:
        cfg = yaml.load(c)
        if not cfg:
            error("config file '%s' is empty" % config_file)

        for node, hosts in cfg.iteritems():
            for host in hosts:
                result = plink(host)
                if not result:
                    log_status = "not_ok"
                else:
                    for line in result.splitlines():
                        if not is_result_valid(line):
                            log_status = "not_ok"
                        plink_results.append(line)

    # Write log file
    now = datetime.datetime.now()
    log_filename = "%s.log.%s.csv" % (now.strftime("%d-%m-%Y-%H-%M-%S"), log_status)
    with open(log_filename, 'w') as log_file:
        log_file.write("Server ip,Date,Time,Value,Percentage\n")
        for result in plink_results:
            log_file.write("%s\n" % result)


if __name__ == '__main__':
    main()
