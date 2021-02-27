import urllib
import os
import base64
import json
import boto3
from botocore.exceptions import ClientError

# THIS FUNCTION ONLY WORKS WITH 2.7 because of urllib
# ENV Variable example
# IP 10.176.0.4
# JENKINS_USER admin
# JOBNAME foo-auto-tests-mobile-api-qa
# PORT 8080
# REGION_NAME us-west-2

def get_secret(secret_name,region_name):


    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            
    # secret comes back as JSON
    # convert to dictionary
    #must have [0] to be real dictionary
    secrets_dictionary = json.loads(secret)[0]
    
    #go through the dictionary and get the actual pw
    list_of_values = [] 
    for key, value in secrets_dictionary.items() :
        if value != secret_name:
           #print (value)
           list_of_values.append(value)
        
    pw = list_of_values[-1]
    return pw



def lambda_handler(event, context):
    
    USER = os.environ['JENKINS_USER']
    IP = os.environ['IP']
    PORT = os.environ['PORT']
    # foo-auto-tests-mobile-api-qa-aws_trigger = dummy
    # foo-auto-tests-mobile-api-qa = real
    JOBNAME = os.environ['JOBNAME']
    #APIKEY = "foo"
    
    # calling the first time to get jenkins admin pw from secrets ma
    SECRET_NAME = 'jenkins_password'   # Name of the secret in AWS Secret manager
    REGION_NAME = os.environ['REGION_NAME']
    PW = get_secret(SECRET_NAME,REGION_NAME)
    
    #calling 2nd time to retrieve the APIKEY
    SECRET_NAME = 'jenkins_apikey'   # Name of the secret in AWS Secret manager for Jenkins job API key
    APIKEY = get_secret(SECRET_NAME,REGION_NAME)
    
    
    
    #creating the LONGSTRING so that we can pass it to urlib
    LONGSTRING = "http://" + USER + ":" + PW + "@" + IP + ":" + PORT + '/job/' + JOBNAME  + '/build?token=' + APIKEY
    #print(LONGSTRING)
    print('Triggering the jenkins job')
    
    try:
        #actual example of a call
        #x = urllib.urlopen('http://USER:PW@1.1.1.1:8080/job/foo-auto-tests-mobile-api-qa/build?token=APIKEY')
        print("_____________________________________________________________")
        # This is where we actually start the jenkins job
        x = urllib.urlopen(LONGSTRING)
        print("_____________________________________________________________")

    except Exception as e:
        print(str(e))

    
    return "Trigger Initiated"
