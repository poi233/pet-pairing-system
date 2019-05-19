import json
import boto3
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr

dynamodb = boto3.resource('dynamodb')
#pet_table = dynamodb.Table('petpair-pet')
user_table = dynamodb.Table('petpair-user')
client = boto3.client('dynamodb')
response = client.list_tables()

def lambda_handler(event, context):
    # TODO implement
    user_email = event['user_email']
    email_tmp = user_email.replace("@", "-")
    table = 'petpair-prediction-{}'.format(email_tmp)
    if table in response['TableNames']:
        table_found = True
    else:
        table_found = False
    tmp = user_table.query(KeyConditionExpression=Key('user_email').eq(user_email))
    if table_found:
        pet_table = dynamodb.Table(table)
    else:
        pet_table = dynamodb.Table('petpair-pet')
    if 'start_key' in event:
        result = pet_table.scan(
            Limit=50,
            ExclusiveStartKey={
                'pet_id': event['start_key']
            },
            FilterExpression=Attr('status').eq(0),
        )
    else:
        result = pet_table.scan(Limit=50)
    ans = dict({'Items':[]})
    for i in range(len(result['Items'])):
        pet_id = result['Items'][i]['pet_id']
        if 'pets' in tmp['Items'][0] and len(tmp['Items']) > 0 and pet_id in tmp['Items'][0]['pets']:
            continue
        else:
            if len(tmp['Items']) > 0 and "wishlist" in tmp['Items'][0] and pet_id in tmp['Items'][0]['wishlist']:
                result['Items'][i]['like'] = '1'
            else:
                result['Items'][i]['like'] = '0'
            ans['Items'].append(result['Items'][i])

    return {
        "statusCode": 200,
        "body": ans['Items'],
        "start_key": result['LastEvaluatedKey'],
        # "body": result,
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': "*"
        }
    }