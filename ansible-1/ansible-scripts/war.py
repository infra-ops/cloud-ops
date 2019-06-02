import requests,subprocess
from subprocess import PIPE
import re
from requests.auth import HTTPBasicAuth
import json
requests.packages.urllib3.disable_warnings()



def get_infos():
    headers = {'Content-Type': 'application/json'}
    r = requests.get('http://localhost:8085/job/war-deploy-1/lastBuild/consoleText', auth=HTTPBasicAuth('xxxx', 'xxxx'),  headers=headers, verify=False)
    re = r.text
    lines=re.split("\n")
    war_id=""
    for line in lines:
	line = line.rstrip("\n")
	if line.isdigit():
		war_id=line
		break
    cmd = 'curl -s -k -u nik:iis123 "http://localhost:8085/job/war-deploy-1/lastBuild/consoleText"  '+"| tail -n 50 | sed -n '/upload/p' | egrep -o mavenproject1-1.0-SNAPSHOT.*war"+' | cut -d " " -f1'
    exe=subprocess.Popen(cmd,shell=True,stdout=PIPE)
    out, err= exe.communicate()
    war_name=out.rstrip('\n')
    data=[war_name,war_id]
    return data


def post_war(build_id,war_name):
    #print build_id
    #print war_name
    headers = {'Content-Type': 'application/json'}
    body  = {"extra_vars":{'build_no': str(build_id), 'ear_ver': str(war_name)}}
    r = requests.post('http://127.0.0.1/api/v2/job_templates/21/launch/', auth=HTTPBasicAuth('xxxx', 'xxxxx'),  headers=headers, json=body,  verify=False)
    print r.text
data = get_infos()
post_war(data[1],data[0])
