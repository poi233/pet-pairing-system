import json
import boto3
import base64
import time
import requests

db = boto3.client('dynamodb')
s3 = boto3.client('s3')
bucket = 'pet-pair-picture'
host = 'https://s3.amazonaws.com'
eshost = 'https://vpc-petparing-vpc-3fx4z2v6xqknlwatal3cwygtze.us-east-1.es.amazonaws.com'
index = 'pets'
type = 'Pet'
esurl = eshost + '/' + index + '/' + type + '/'

def lambda_handler(event, context):
    user_email = event['user_email']
    pet_id = user_email + "," + str(time.time())
    file_name = pet_id + '.jpg'
    url = host + '/' + bucket + '/' + file_name
    print(url)
    # add to dynamodb - pet
    db.put_item(
        TableName='petpair-pet',
        Item={
            'pet_id':{
                'S': pet_id
            },
            'name': {
                "S" : event['name']
            },
            'age': {
                "N" : event['age']
            },
            'status': {
                "N" : "0"
            },
            'gender': {
                "N" : event['gender']
            },
            'breed': {
                "S" : event['breed']
            },
            'description': {
                "S" : event['description']
            },
            'pet_image': {
                "S" : url
            },
            'owner': {
                "S" : user_email
            }
        }
    )
    # add file to s3
    file_content = base64.b64decode(event['file_content'])
    s3.put_object(ACL='public-read-write', Body=file_content, Bucket=bucket, Key=file_name)
    # add to dynamodb - user
    db.update_item(TableName='petpair-user',
               Key={'user_email':{'S':user_email}},
               UpdateExpression="ADD pets :element",
               ExpressionAttributeValues={":element":{"SS":[pet_id]}})
    # add to elastic search
    add_to_es(
        pet_id,
        dict({
            "breed":event["breed"].lower(),
            "description":event["description"].lower()
            })
    )
    return {
        "statusCode": 200,
        "body": {},
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }

def add_to_es(id, data):
    region = 'us-east-1'  # e.g. us-east-1
    service = 'es'
    credentials = boto3.Session().get_credentials()
    headers = {"Content-Type": "application/json"}
    r = requests.put(esurl + id, json=data, headers=headers)

