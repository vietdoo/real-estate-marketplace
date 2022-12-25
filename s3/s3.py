import boto
import boto3
import sys
from boto.s3.key import Key

class S3():
    def __init__(self):
        self.client = boto3.client("s3")

    def upload_file_to_s3(self, bucket_name, input_name, output_name):
        self.client.upload_file(   
            Filename = input_name,
            Bucket = bucket_name,
            Key = output_name)
