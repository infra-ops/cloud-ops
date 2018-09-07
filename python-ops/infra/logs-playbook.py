# -*- coding: utf-8 -*-

"""
cron executed script which processes Deployment Task Queue
"""
import re
import csv
import cStringIO
from logging import getLogger
import subprocess
import sys
from tabulate import tabulate
from time import sleep

from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, IntegrityError
from lockfile import LockFile, LockTimeout

from searchstax.deployment.models import (
    DedicatedDeployment,
)
from searchstax.settings import TECHOPS_EMAIL, DEV_EMAIL, PROJECT_ROOT

try:
    from subprocess import DEVNULL
except ImportError:
    import os

    DEVNULL = open(os.devnull, 'wb')

LOGGER = getLogger('management_commands')

class Command(BaseCommand):

    def handle(self, *args, **options):
        deployments = DedicatedDeployment.objects.filter(
            status=DedicatedDeployment.RUNNING,
            terminated=None
        )

        tasks_regex = [
            ('TASK \[Gathering Facts\]', 'ok: \[(ss\d{6}-\d)'),
            ('TASK \[Read disks and mount points\]', 'Device: (.*) Mount Point: (.*)\"'),
            ('TASK \[Find solr log4j path\]', '\"Solr log4j path: (.*)\"'),
            ('TASK \[Find solr log dir path\]', '\"Solr logs path: (.*)\"'),
            ('TASK \[Find zookeeper log dir path\]', '\"Zookeeper log path: (.*)\"'),
            ('PLAY RECAP', )
        ]

        header = (
            'Deployment Name', 'SSID', 'Server', 'Disks (Device\tMount Point)',
            'Log4j Path', 'Solr log path', 'Zookeeper log path')

        all_rows = []

        for deployment in deployments:
            if deployment.custom:
                all_rows.append([
                    deployment.name, deployment.uid,
                    'CUSTOM Deployment - Skipped'])
                continue

            if deployment.cloud_private:
                all_rows.append([
                    deployment.name, deployment.uid,
                    'Private Deployment - Skipped'])
                continue

            task = [
                '%s' % sys.executable,
                '%s/manage.py' % PROJECT_ROOT,
                'playbook',
                '%s' % deployment.uid,
                'check_logs_path.yml'
            ]

            try:
                command_output = subprocess.check_output(
                    task, stderr=subprocess.STDOUT)

                for server_output in command_output.split("running for dns")[1:]:

                    server_row = [deployment.name, deployment.uid]
                    all_rows.append(server_row)
                    if 'UNREACHABLE' in server_output:
                        server = re.findall('(ss\d{6}-\d)', server_output)
                        server_row.append("%s - UNREACHABLE" % server[0])
                        continue

                    for i in range(len(tasks_regex) - 1):
                        re_task_1 = tasks_regex[i]
                        re_task_2 = tasks_regex[i + 1]

                        task_output = re.search("%s([\s\S]*)%s" % (
                            re_task_1[0], re_task_2[0]), server_output)
                        if not task_output:
                            continue

                        task_output = task_output.groups()[0]
                        task_result = re.findall(re_task_1[1], task_output)
                        if not task_result:
                            continue

                        server_row.append("\n".join(
                            ["\t".join(group) if type(group) == tuple else group
                             for group in task_result]))

            except Exception as e:
                print e
                print getattr(e, 'output', '')

        with open('deployment_disks.csv', 'wb') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',')
            csvwriter.writerow(header)
            csvwriter.writerows(all_rows)

            print(tabulate(all_rows, headers=header, tablefmt="grid"))
