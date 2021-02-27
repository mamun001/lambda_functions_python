import os
import boto3
import string
import random

def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))


def lambda_handler(event, context):
  
  cloudfront_instance = boto3.client('cloudfront')
  dist = cloudfront_instance.list_distributions()
  files = ["/index.html", "/swagger.html", "/foo_mobile_swagger.json", "/foo_swagger.json", "/swagger-mobile.json" ]
  BUCKET = os.environ['BUCKET']
  
  for x in range(0, len(dist)):
      print (dist["DistributionList"]["Items"][x]["Origins"]["Items"][0]["Id"])
      THIS_BUCKET=(dist["DistributionList"]["Items"][x]["Origins"]["Items"][0]["Id"])
      
      if BUCKET == THIS_BUCKET:
        print ("Found matching cloudfront distribution for given S3 origin website bucket")
        DISTID = dist["DistributionList"]["Items"][x]["Id"]
        print()
        print("DISTRIBUTION_ID=" + DISTID)
        print()
        cloudfront_instance.create_invalidation(
          DistributionId=DISTID,
          InvalidationBatch={
            'Paths': {
            'Quantity': len(files),
            'Items': ['/{}'.format(f) for f in files]
          },
          'CallerReference': string_generator()
     }
    )
      
  
    
  
  
  
