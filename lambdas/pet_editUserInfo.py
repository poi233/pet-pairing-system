import json
import boto3
from boto3.dynamodb.conditions import Key

db = boto3.client('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    db.update_item(TableName='petpair-user',
              Key={'user_email':{'S':event['user_email']}},
              AttributeUpdates={
                    'name': {
                        'Value': {"S" : event['name']},
                        'Action': 'PUT'
                    },
                    'address': {
                        'Value': {"S" : event['address']},
                        'Action': 'PUT'
                    },
                    'description': {
                        'Value': {"S" : event['description']},
                        'Action': 'PUT'
                    }
                }
              )
    return {}
