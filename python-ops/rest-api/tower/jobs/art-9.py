import csv
import json,socket
import requests
import re
import argparse
from datetime import datetime
from requests.auth import HTTPBasicAuth
import re
import subprocess
from email import Encoders
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from ansible.constants import DEFAULT_VAULT_ID_MATCH
from ansible.parsing.vault import VaultLib
from ansible.parsing.vault import VaultSecret
from termcolor import colored

headers = {'Content-Type': 'application/json' }
arti_name="empty"
page_var=1
arti_name="null"
while True:
		try:
          u4 = "http://localhost/api/v2/jobs/6/job_events/?page=%s&page_size=100"%str(page_var)
			    r4 = requests.get(u4,auth=HTTPBasicAuth('admin', 'password'),headers=headers,verify=False)
			    data4 = json.loads(r4.text)
			    numb = len(data4["results"])
			    for j in range(0,numb):
					try:
						if data4["next"] == "null":
							if int(data4["results"][j]["job"]) == 6:
								arti_name=data4["results"][j]["event_data"]["playbook_uuid"]
								if str(arti_name) == "":
									arti_name="no artifact"
								break
							else:
								continue
						else:
							if int(data4["results"][j]["job"]) == 6:
								arti_name=data4["results"][j]["event_data"]["playbook_uuid"]
								if str(arti_name) == "":
									arti_name="no artifact"
								page_var=page_var+1
							else:
								continue
					except:
						continue
		except:
			break
print "%s"%arti_name
