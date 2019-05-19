import json
import boto3

db = boto3.client("dynamodb")

def lambda_handler(event, context):
    # It sets the user pool autoConfirmUser flag after validating the email domain
    event['response']['autoConfirmUser'] = False

    # Split the email address so we can compare domains
    email = event['request']['userAttributes']['email']
    # name = event['request']['userAttributes']['username']

    db.put_item(
        TableName='petpair-user',
        Item={
            'user_email':{
                'S': email
            }
            # 'name':{
            #     'S': name
            # }
        }
    )
    # Return to Amazon Cognito
    return event
