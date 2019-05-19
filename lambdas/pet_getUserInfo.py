import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('petpair-user')

def lambda_handler(event, context):
    # TODO implement
    user_email = event['queryStringParameters']['user_email']
    user_info = user_table.query(KeyConditionExpression=Key('user_email').eq(user_email))
    print(user_info)
    tmp = dict()
    if user_info['Items'] is not None:
        tmp = dict({
            "user_email": user_info['Items'][0]['user_email'],
            "name": user_info['Items'][0]['name'] if "name" in user_info['Items'][0] else "",
            "address": user_info['Items'][0]['address'] if "address" in user_info['Items'][0] else "",
            "description": user_info['Items'][0]['description'] if "description" in user_info['Items'][0] else ""
        })
    return {
        'statusCode': 200,
        'body': json.dumps(tmp),
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }

    }
