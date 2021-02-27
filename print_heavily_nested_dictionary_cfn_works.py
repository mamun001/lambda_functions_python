import os
import boto3
import string
import random

   
def pretty(d, indent=0):
   for key, value in d.items():
      print('\t' * indent + str(key))
      if isinstance(value, dict):
         pretty(value, indent+1)
      else:
         print('\t' * (indent+1) + str(value))
         

def lambda_handler(event, context):


# CallerReference has to be uniq for each call
# file is an array of list of files, but each one has to start with /
  
  cloudfront_instance = boto3.client('cloudfront')
  dist = cloudfront_instance.list_distributions()
  pretty(dist)
  
  
