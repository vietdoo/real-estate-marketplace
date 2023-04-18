import requests
import pymongo
import sys
import json
from bson.json_util import dumps
from bson.json_util import loads
import pandas as pd
import matplotlib.pyplot as plt
import time

import boto
import boto3
import sys
from boto.s3.key import Key
from s3 import S3


f = open('clean.json')
data = json.load(f)

df = pd.DataFrame(data)


def data_for_mongo(data):
    new_data = []
    for item in data:
        try:
            new_item = {}
            new_item['long'] =  item['longitude']
            new_item['lat'] = item['latitude']
            new_item['title'] = item['subject']
            new_item['price'] = item['price']
            new_item['dist'] = item['area_name']
            new_item['img'] = item['image']
            new_item['url'] = item['url']
            new_item['rooms'] = item['rooms']
            new_item['size'] = item['size']
            
            new_data.append(new_item)
        except:
            pass
        
        
    
    return new_data

with open('mongo.json', 'w') as f:
    json.dump(data_for_mongo(df.to_dict(orient = 'records')), f)


S3_client = S3()
S3_client.upload_file_to_s3(bucket_name = 'tigerlake', input_name = 'mongo.json', output_name = 'mongo.json')

