import json
import boto3
db = boto3.client("dynamodb")

def lambda_handler(event, context):
    # TODO implement
    db.update_item(TableName='petpair-user',
               Key={'user_email':{'S':event['user_email']}},
               UpdateExpression="ADD wishlist :element",
               ExpressionAttributeValues={":element":{"SS":[event['pet_id']]}})

    return {
        'statusCode': 200,
        'body': {}
    }
