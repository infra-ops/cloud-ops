from fabric.api import run, env

env.hosts = ['192.168.10.25']

def taskA():
    run('ls -ld /opt/apps/solr')

def taskB():
    run('whoami')
