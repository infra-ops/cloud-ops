import requests
import json
import sys

url = "https://1scjp21jd2.execute-api.us-east-1.amazonaws.com/prod/service"

headers = {
"Content-Type": "application/json"
}

input  = sys.argv[1]

with open(input) as payload:
    data = json.load(payload)
    response = requests.post(url, headers=headers, data= json.dumps(data))
    print response.text
