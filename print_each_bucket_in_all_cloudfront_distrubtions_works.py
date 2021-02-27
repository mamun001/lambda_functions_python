
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



  
  cloudfront_instance = boto3.client('cloudfront')
  dist = cloudfront_instance.list_distributions()
  
  print ("1_______________________________________")
  
  pretty(dist)
  
  print ("222_______________________________________")
  
  for key, value in dist.items() :
     print (key)
  
  print ("333_______________________________________")
  
  #print (dist["DistributionList"]["Items"][0]["ARN"])
  #print (dist["DistributionList"]["Items"][0]["Origins"])
  #print (dist["DistributionList"]["Items"][0]["Origins"]["Items"])
  #print (dist["DistributionList"]["Items"][0]["Origins"]["Items"][0]["Id"])
  
  for x in range(0, 5):
      print (dist["DistributionList"]["Items"][x]["Origins"]["Items"][0]["Id"])
  
    
  print ("444_______________________________________")
  
  
