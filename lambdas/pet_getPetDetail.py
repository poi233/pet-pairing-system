import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
pet_table = dynamodb.Table('petpair-pet')
user_table = dynamodb.Table('petpair-user')

def lambda_handler(event, context):
    # TODO implement
    user_email = event['queryStringParameters']['user_email']
    pet_id = event['queryStringParameters']['pet_id']
    owner_email = pet_id.split(",")[0]
    user = user_table.query(KeyConditionExpression=Key('user_email').eq(user_email))['Items'][0]
    pet = pet_table.query(KeyConditionExpression=Key('pet_id').eq(pet_id))['Items'][0]
    owner = user_table.query(KeyConditionExpression=Key('user_email').eq(owner_email))['Items'][0]
    if 'wishlist' in user and len(user['wishlist']) > 0 and pet_id in user['wishlist']:
        owner['like'] = "1"
    else:
        owner['like'] = "0"
    if 'wishlist' in owner:
        del owner['wishlist']
    if 'pets' in owner:
        del owner['pets']
    pet['status'] = str(pet['status'])
    pet['age'] = str(pet['age'])
    pet['gender'] = str(pet['gender'])
    print(owner)
    print(pet)
    ans = dict({
        "user":owner,
        "pet":pet
        })
    return {
        "statusCode": 200,
        "body": json.dumps(ans),
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': "*"
        }
    }