#!/usr/bin/env python

import argparse
import logging
import os
import sys

from StringIO import StringIO
from datetime import datetime

import boto3


def error(msg, and_exit=True):
    print("ERROR: %s" % msg)
    if and_exit:
        sys.exit(-1)

try:
    import yaml
except ImportError as ie:
    LIB_MAP = {'yaml': 'PyYAML'}
    m = ie.message
    missing_mod = m[m.rfind(" "):].strip()
    msg = "missing python module '%s' (please install manually)\n" % missing_mod\
        + "  use: pip install %s" % LIB_MAP.get(missing_mod, missing_mod)
    error(msg)

AWS_INSTANCE_YAML_FILE = 'ec2.yml'
START_MODE = 'start'
STOP_MODE = 'stop'
TERMINATE_MODE = 'terminate'

LOG_BUCKET = 'dev-log-3'
LOG_INCR_GUARD = 200


class Logger(object):
    def __init__(self, cmd, date):
        self._s3 = boto3.resource('s3')
        self._date = date
        self._logger = logging.getLogger(cmd)
        self._filename = "%s-instance-%s.log" % (
            date.strftime("%d-%m-%y-%H-%M"),
            cmd
        )
        self._init_logger(self._logger)
        self._logger.setLevel(logging.INFO)
        self._logger.info("date      time         instance-id             status")
        self._logger.info("")  # empty line

    def _init_logger(self, logger):
        if os.path.isfile(self._filename):
            error("logfile '%s' still exists - please remove first or wait a minute!" % self._filename)
        logger.addHandler(logging.FileHandler(self._filename))

    def write(self, instance_id, status, expected_result):
        msg = "%s  %s     %s     %s %s" % (
            self._date.strftime("%d/%m/%y"),
            self._date.strftime("%H:%M.%S"),
            instance_id,
            status,
            "" if expected_result else "!!!"
        )
        self._logger.info(msg)

    def _determ_next_log_key(self, bucket_name):
        date_folder = "%s-%s-%s" % (self._date.day, self._date.month, self._date.year)
        incr_folder = 1
        subfolder = None
        found = False
        while incr_folder <= LOG_INCR_GUARD:
            subfolder = "%s/%s" % (date_folder, incr_folder)
            match = self._s3.meta.client.list_objects(Bucket=bucket_name, Prefix=subfolder)
            if 'Contents' not in match or len(match['Contents']) == 0:
                found = True
                break
            incr_folder += 1
        if not found:
            error("could not move logfile '%s' to bucket folder '%s' (LOG_INCR_GUARD)" % (
                self._filename, date_folder))
        return "%s/%s" % (subfolder, os.path.basename(self._filename))

    def move_to_bucket(self, bucket_name):
        log_key = self._determ_next_log_key(bucket_name)
        self._do_bucket_move(bucket_name, log_key)
        return log_key

    def _do_bucket_move(self, bucket_name, log_key):
        self._logger.handlers.pop(0).close()
        self._s3.meta.client.upload_file(self._filename, bucket_name, log_key)
        os.remove(self._filename)


class BufferLogger(Logger):
    def __init__(self, cmd, date):
        Logger.__init__(self, cmd, date)

    def _init_logger(self, logger):
        self._log_stream = StringIO()
        logger.addHandler(logging.StreamHandler(self._log_stream))

    def _do_bucket_move(self, bucket_name, log_key):
        stream_handler = self._logger.handlers.pop(0)
        self._log_stream.seek(0)
        self._s3.meta.client.upload_fileobj(self._log_stream, bucket_name, log_key)
        stream_handler.close()


def get_instances(yaml_file):
    if not os.path.isfile(yaml_file):
        error("instance file not exists: %s" % yaml_file)

    result = {}
    with open(yaml_file) as f:
        result = yaml.load(f)
    return result


def handle_response(r, mode, logger):
    # boto3 status are:
    #   pending, running, shutting-down, , stopping, stopped
    instance = r['InstanceId']
    status = r['CurrentState']['Name']
    if mode == START_MODE:
        logger.write(instance, status, status == "running")
    elif mode == STOP_MODE:
        logger.write(instance, status, status == "stopped")
    elif mode == TERMINATE_MODE:
        logger.write(instance, status, status == "terminated")
    else:
        raise NotImplementedError("INTERNAL ERROR: unknown mode '%s'" % mode)
    print("%s\tinstance   %s" % (status, instance))


def start_instances(region, instances, logger):
    ec2 = boto3.client('ec2', region_name=region)
    for r in ec2.start_instances(InstanceIds=instances)['StartingInstances']:
        handle_response(r, START_MODE, logger)


def stop_instances(region, instances, logger):
    ec2 = boto3.client('ec2', region_name=region)
    for r in ec2.stop_instances(InstanceIds=instances)['StoppingInstances']:
        handle_response(r, STOP_MODE, logger)


def terminate_instances(region, instances, logger):
    ec2 = boto3.client('ec2', region_name=region)
    for r in ec2.terminate_instances(InstanceIds=instances)['TerminatingInstances']:
        handle_response(r, TERMINATE_MODE, logger)


def lambda_handler(event, context):
    """AWD Lambda handler function."""
    if 'command' not in event:
        error("missing key 'command' in event")
    cmd = event['command']
    if cmd not in [START_MODE, STOP_MODE, TERMINATE_MODE]:
        error("invalid command '%s'" % cmd)

    started = datetime.now()
    logger = BufferLogger(cmd, started)
    for region, instances in get_instances(AWS_INSTANCE_YAML_FILE).iteritems():
        if cmd == START_MODE:
            start_instances(region, instances, logger)
        elif cmd == STOP_MODE:
            stop_instances(region, instances, logger)
        elif cmd == TERMINATE_MODE:
            terminate_instances(region, instances, logger)
        else:
            raise NotImplementedError("invalid command '%s'" % cmd)
    log_bucket_name = event.get('log-bucket', LOG_BUCKET)
    log_bucket_key = logger.move_to_bucket(log_bucket_name)
    return "%s instances (log: %s/%s)" % (cmd, log_bucket_name, log_bucket_key)


def main():
    """ Main method used from commandline."""
    parser = argparse.ArgumentParser()
    parser.add_argument('INSTANCES_FILE', help="instances control file (e.g: %s)" % AWS_INSTANCE_YAML_FILE)
    parser.add_argument('-s', help='[start|stop] instances (default: start)',
                        metavar='COMMAND', default='start')
    parser.add_argument('-t', help='terminate instances', action='store_true')
    parser.add_argument('-d', help='bucket for logs (if not given, logs will be stored locally)',
                        metavar='BUCKET_NAME')
    args = parser.parse_args()

    if args.t:
        cmd = TERMINATE_MODE
    else:
        cmd = args.s
        if cmd not in [START_MODE, STOP_MODE]:
            error("invalid '-s' option '%s' (must be '%s' or '%s')" % (cmd, START_MODE, STOP_MODE))

    started = datetime.now()
    logger = Logger(cmd, started)
    print("started script at %s time\n" % started.strftime("%H:%M.%S"))
    for region, instances in get_instances(args.INSTANCES_FILE).iteritems():
        if cmd == START_MODE:
            start_instances(region, instances, logger)
        elif cmd == STOP_MODE:
            stop_instances(region, instances, logger)
        elif cmd == TERMINATE_MODE:
            terminate_instances(region, instances, logger)
        else:
            raise NotImplementedError("INTERNAL ERROR: invalid command '%s'" % cmd)
    ended = datetime.now()
    print("\nstopped script at %s time" % ended.strftime("%H:%M.%S"))

    if args.d:
        log_bucket_key = logger.move_to_bucket(args.d)
        print("moved logfile to: %s" % log_bucket_key)


if __name__ == '__main__':
    main()
