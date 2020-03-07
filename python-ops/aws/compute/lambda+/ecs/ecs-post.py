#!/usr/bin/python
##execution process : python post.py
import requests
import json
import subprocess
def image_no():
	p = subprocess.Popen("aws ecr describe-images --repository-name connector-dev --query 'sort_by(imageDetails,& imagePushedAt)[-1].imageTags[0]' --output text",shell=True, stdout=subprocess.PIPE)
	pp=p.stdout.read().strip()
	return pp
image_no=image_no()
def json_body():
        json={
"region":"us-east-1",
"service":"python-task",
"cluster":"connector-clus",
"image":"758637906269.dkr.ecr.us-east-1.amazonaws.com/connector-dev:"+image_no,
"desiredCount":1

}
        return json
def rest_hit():
           url="https://1scjp21jd2.execute-api.us-east-1.amazonaws.com/prod/service"
           headers = {
                  "Content-Type": "application/json",
		"x-api-key":"6bKBEiiGF48qgdLymE4tO2GuTyklu8IZ6P1doBh8"
}
	   payload=json_body()
           response = requests.post(url, headers=headers, data=json.dumps(payload))
           print response.text
rest_hit()
