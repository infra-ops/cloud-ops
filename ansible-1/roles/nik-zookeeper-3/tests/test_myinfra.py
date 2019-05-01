def test_passwd_file(host):
    passwd = host.file("/etc/passwd")
    assert passwd.contains("root")
    

def test_config_file(File):
    config_file = File('/opt/apps/solr/bin/solr.in.sh')
    assert config_file.contains('/opt/data/solr/logs')  # todo make it a regex
    assert config_file.is_file

def test_command_output(Command):
    command = Command('ls -ld /opt/apps/solr')
#    assert command.stdout.rstrip() == '/opt/data/solr/logs'
    assert command.rc == 0


def test_command_output(Command):
    command2 = Command('hostname')
    assert command2.rc == 0

