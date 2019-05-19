import json
import boto3
import requests

db = boto3.client("dynamodb")
s3 = boto3.client("s3")
bucket = 'pet-pair-picture'
eshost = 'https://vpc-petparing-vpc-3fx4z2v6xqknlwatal3cwygtze.us-east-1.es.amazonaws.com'
index = 'pets'
type = 'Pet'
esurl = eshost + '/' + index + '/' + type + '/'

def lambda_handler(event, context):
    # TODO implement
    user_email = event['pet_id'].split(",")[0]
    db.update_item(
        TableName='petpair-user',
        Key={'user_email':{'S':user_email}},
        UpdateExpression="DELETE pets :elem",
        ExpressionAttributeValues={":elem":{"SS":[event['pet_id']]}})
    db.delete_item(
        TableName='petpair-pet',
        Key={'pet_id':{'S':event['pet_id']}}
    )
    s3.delete_object(
        Bucket=bucket,
        Key=event['pet_id'] + ".jpg")
    requests.delete(esurl + event['pet_id'])
    return {}
