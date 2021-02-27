
# version 9.9.2019
#
#  usage: python3 this_file.py
#   MUST BE PYTHON3
#   
#  This really works!
#
import boto3
import sys
import time

bucketname = input("bucketname to delete all versions and bucket itself: ")  # Python 3
print("You entered: " + bucketname)
print(" " )
print(" " )
print(" " )
print("Are you sure you want to completely wipeout: " + bucketname)
answer = input("Type y or Y or yes or Yes or YES if you are sure: ")

if answer in ['y', 'Y', 'yes', 'Yes', 'YES']:
    print("Going ahead with deletion of all versions of this bucket and then deleting the bucket")
    #print(bucketname) <--works
    time.sleep(5) 
    session = boto3.Session()
    s3 = session.resource(service_name='s3')
    #bucket = s3.Bucket('ddm-chairmanscorner-qa')  <--works
    #bucket = s3.Bucket('dev-ddm-uploads') <--works
    #bucket = s3.Bucket(bucketname)  <--works
    bucket = s3.Bucket(bucketname)  
    bucket.object_versions.delete()
    bucket.delete()
    sys.exit()
else:
   sys.exit()




