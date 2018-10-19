#/usr/bin/python

#python jenkinscool.py -i https://updates.jenkins-ci.org/download/plugins/blueocean/1.0.1/blueocean.hpi
#python jenkinscool.py -p  p5.yml

import yaml
import argparse
import subprocess



#def restart_jenkins():
#    subprocess.call("sudo systemctl restart jenkins", shell=True)



try:
    import yaml
except ImportError as ie:
    LIB_MAP = {'yaml': 'PyYAML'}
    m = ie.message
    missing_mod = m[m.rfind(" "):].strip()
    msg = "missing python module '%s' (please install manually)\n" % missing_mod\
        + "  use: pip install %s" % LIB_MAP.get(missing_mod, missing_mod)
    error(msg)




def read_yaml(filename):
    response = None
    with open(filename, 'r') as stream:
        try:
            response = yaml.load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return response

def send_command_url(url):
    resp = subprocess.check_output(['wget','%s'%url])
    print resp

def copy_command():
    resp = subprocess.call(
        'mv *.hpi  /opt/apps/jenkins-data/plugins', shell=True)
    if int(resp) == 0:
      print "successfully copied files"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i")
    parser.add_argument("-p")
    args = parser.parse_args()
    if (args.i is not None) and (args.p is None):
            yaml_dict = read_yaml(args.i)
            plugin_dict = yaml_dict.keys()
            for plugin in plugin_dict:
                print "\nInstalling Plugin: %s"%plugin
                for urx in yaml_dict.get(plugin):
                 send_command_url(urx)
            copy_command()
            print "Please restart jenkins for changes to reflect"
 #           restart_jenkins()
    elif (args.i is None) and (args.p is not None):
            print "\n Downloading from url"
            send_command_url(args.p)
            copy_command()
            print "Please restart jenkins for changes to reflect"
#            restart_jenkins()


if __name__ == '__main__':
    main()
