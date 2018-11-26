#!/usr/bin/env python3
#import module
import csv
import json
 
 
with open("/var/lib/jenkins/workspace/tom-test/tmp_tomcat-1-task.json") as raw:
    data=json.load(raw)
    param_change=25
    to_change=str(param_change)
    data["containerDefinitions"][0]["image"]=f'758637906269.dkr.ecr.us-east-1.amazonaws.com/connector-dev:{to_change}'
   
    with open("/var/lib/jenkins/workspace/tom-test/tmp_tomcat-1-task.json ", mode="w") as out_raw:
        json.dump(data,out_raw, indent=4)
