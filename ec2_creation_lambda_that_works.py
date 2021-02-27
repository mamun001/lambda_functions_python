

# this is from https://linuxacademy.com/hands-on-lab/fa909442-ef96-43fc-97ad-a52892a1401b/
# Linux academy
# Pythion 3.7
# in ENVs of this lambad function:
# put in values for AMI, INSTANCE_TYPE, KEY_NAME and SUBNET_ID
# and give it role that has permison for ec2 and lamba 
# when running, use dummy event like  { "key1" : "value1" }
# totally worked 2020.01.17

import os
import boto3

AMI = os.environ['AMI']
INSTANCE_TYPE = os.environ['INSTANCE_TYPE']
KEY_NAME = os.environ['KEY_NAME']
SUBNET_ID = os.environ['SUBNET_ID']

ec2 = boto3.resource('ec2')


def lambda_handler(event, context):

    instance = ec2.create_instances(
        ImageId=AMI,
        InstanceType=INSTANCE_TYPE,
        KeyName=KEY_NAME,
        SubnetId=SUBNET_ID,
        MaxCount=1,
        MinCount=1
    )

    print("New instance created:", instance[0].id)

