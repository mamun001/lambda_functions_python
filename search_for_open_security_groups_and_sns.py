import json
import boto3
region ="us-west-2"
sns_arn = "arn:aws:sns:us-west-2:123456789:foo_dev_qa_alerts"
#inbound_cidr = '10.176.0.0/16'   #for testing purposes
inbound_cidr = '0.0.0.0/0'
email_subject = 'We have at least 1 Security Group that is wide open'

         

def lambda_handler(event, context):

    ec2 = boto3.client('ec2')
    response = ec2.describe_security_groups(
    Filters=[
        {
            'Name': 'ip-permission.cidr',
            'Values': [
                inbound_cidr,
            ]
        },
    ],
 )
    
    
    #response is a dcitionary. Go through the dictionary and convert into a list. This is a must for further steps
    list_of_values = [] 
    for key, value in response.items() :
           list_of_values.append(value)
        
    
    #print(len(list_of_values))
    # this is key. if this is 0, then we have no match
    # if this is 1 or more, then we have at least 1 BAD SG rule.
    BADCOUNT=len(list_of_values[0])
    print(BADCOUNT)
    email_body = ''
    
    if BADCOUNT >= 1:
        print('We have at least 1 BAD rule')
        for i in range(0,BADCOUNT,1):
            print(list_of_values[0][i]["GroupName"])
            email_body = email_body + " " + list_of_values[0][i]["GroupName"]
            
        message = {"Open": "Security_Group"}
        email_body = email_body
        sns_client = boto3.client('sns')
        sns_response = sns_client.publish(
            TargetArn=sns_arn,
            Message=json.dumps({'default': json.dumps(message),
                        'sms': 'we have 1 SG that is wide open',
                        'email': email_body}),
            Subject=email_subject,
            MessageStructure='json'
        )
            
    else:
        print("GOOD. NO BAD SECURITY GROUP FOUND")

    
