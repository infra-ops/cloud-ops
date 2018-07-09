#!/bin/python

#Need to install requests package for python
#easy_install requests
import requests
import sys
import datetime
import requests
import argparse

###time string usage
current_time = datetime.datetime.now()
current_time_string = current_time.strftime("%d-%b-%Y-%H-%M")

###argparse usage
parser = argparse.ArgumentParser(description="testing")
parser.add_argument('-i', '--ip', dest='ip', default='localhost', help='IP address the server will listen on')
args = parser.parse_args()
#SERVER_IP = sys.argv[1]
###program body
# Set the request parameters
url = 'https://xxxxx.service-now.com/api/now/table/incident'
# Eg. User name="admin", Password="admin" for this code sample.
user = 'xxxx'
pwd = 'xxxxx'
# Set proper headers
headers = {"Content-Type":"application/json","Accept":"application/json"}
# Do the HTTP request
response = requests.post(url, auth=(user, pwd), headers=headers ,data="{\"short_description\":\"Nginx Down On " + args.ip + " AT " + str(current_time_string) + " \"}")
#response = requests.post(url, auth=(user, pwd), headers=headers ,data="{\"short_description\":\"hello\",\"description\":\"world\",\"state\":\"2\"}")
# Check for HTTP codes other than 200
if response.status_code != 200:
    print('Status:', response.status_code, 'Headers:', response.headers, 'Error Response:',response.json())
    exit()
# Decode the JSON response into a dictionary and use the data
data = response.json()
print(data)
