import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
pet_table = dynamodb.Table('petpair-pet')
user_table = dynamodb.Table('petpair-user')

def lambda_handler(event, context):
    # TODO implement
    user_email = event['queryStringParameters']['user_email']
    query = user_table.query(KeyConditionExpression=Key('user_email').eq(user_email))['Items'][0]
    wishlist = query['wishlist'] if 'wishlist' in query else []
    ans = dict({'Items':[]})
    for wish in wishlist:
        tmp = pet_table.query(
            KeyConditionExpression=Key('pet_id').eq(wish)
        )['Items'][0]
        tmp['gender'] = str(tmp['gender'])
        tmp['age'] = str(tmp['age'])
        tmp['status'] = str(tmp['status'])
        ans['Items'].append(tmp)

    print(ans)
    return {
        "statusCode": 200,
        "body": json.dumps(ans),
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': "*"
        }
    }