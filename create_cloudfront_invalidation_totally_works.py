import os
import boto3
import string
import random

DISTRIBUTION_ID = os.environ['DISTRIBUTION_ID']

def string_generator(size=6, chars=string.ascii_uppercase + string.digits):
   return ''.join(random.choice(chars) for _ in range(size))

def lambda_handler(event, context):


# CallerReference has to be uniq for each call
# file is an array of list of files, but each one has to start with /
  
  files = ["/index.html", "/swagger.html", "/foo_mobile_swagger.json", "/foo_swagger.json", "/swagger-mobile.json" ]
  
  print (len(files))
  
  cloudfront = boto3.client('cloudfront')
  cloudfront.create_invalidation(
    DistributionId=DISTRIBUTION_ID,
    InvalidationBatch={
        'Paths': {
            'Quantity': len(files),
            'Items': ['/{}'.format(f) for f in files]
        },
        'CallerReference': string_generator()
     }
    )

