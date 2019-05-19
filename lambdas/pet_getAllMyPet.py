import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
pet_table = dynamodb.Table('petpair-pet')

def lambda_handler(event, context):
    # TODO implement
    user_email = event['queryStringParameters']['user_email']
    ans = dict({'Items':[]})
    pets = pet_table.scan(
            ScanFilter={
                "owner": {
                    'AttributeValueList': [
                        user_email
                    ],
                    'ComparisonOperator': "EQ"
                }
            }
        )
    for pet in pets['Items']:
        # tmp = pet_table.query(
        #     KeyConditionExpression=Key('pet_id').eq(pet)
        # )['Items'][0]
        pet['gender'] = str(pet['gender'])
        pet['age'] = str(pet['age'])
        pet['status'] = str(pet['status'])
        ans['Items'].append(pet)

    print(ans)
    return {
        "statusCode": 200,
        "body": json.dumps(ans),
        # "body": jsong.dumps(pets['Items']),
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': "*"
        }
    }