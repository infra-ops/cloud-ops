#!/bin/python

import yaml
import subprocess
from optparse import OptionParser


def restart_jenkins():
    subprocess.call("sudo systemctl restart jenkins", shell=True)

def read_yaml(filename):
    response = None
    with open(filename, 'r') as stream:
        try:
            response = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return response


def send_command(yaml_dict, plugin_name):
  # Given a plugin name, we need to loop through its dependencies
  hpi_dict = yaml_dict.get(plugin_name)
  for hpi_url in hpi_dict:
    resp = subprocess.check_output([
      'wget',
      '{}'.format(hpi_url)
    ])
    print resp

def copy_command():
    resp = subprocess.call(
        'sudo cp -rf *.hpi  /var/lib/jenkins/plugins/', shell=True)
    print "Exit code from copy operation is: ", resp


def main():
    opt_parser = OptionParser()
    opt_parser.add_option(
        "-i", "--file",
        dest="filename", default=False,
        help="Yaml file name")
    (options, args) = opt_parser.parse_args()
    filename = options.filename
    yaml_dict = read_yaml(filename)
    plugin_dict = yaml_dict.get('plugins')

    print "\n Installing following plugins", plugin_dict
    for plugin in plugin_dict:
        send_command(yaml_dict, plugin)

    copy_command()

    print "Restarting jenkins for changes to take effect"
    restart_jenkins()


if __name__ == '__main__':
    main()
