#/usr/bin/python

import  pymongo
from pymongo import MongoClient
import  json 
from  bson.json_util  import  dumps
# Definition of DB conne
client = MongoClient("mongodb://admin:iis123@127.0.0.1/inventory")
db = client["inventory"]
# acquire inventory collection 
data = db.systems.find({})[0]
output_dict  =  {}
# acquire inventory collection 
output_dict.update(data)
# Remove object ID
del output_dict["_id"]
# Dictionary by JSON format to standard output 
print json.dumps(output_dict,indent=4)
