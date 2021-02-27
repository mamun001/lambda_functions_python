
import os
import boto3

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    
    s3.create_bucket(Bucket='deleteme689543', CreateBucketConfiguration={'LocationConstraint': 'us-west-2'})

    print("Did this work?")
