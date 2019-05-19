import json
import boto3
import base64
import requests

db = boto3.client('dynamodb')
s3 = boto3.client('s3')
bucket = 'pet-pair-picture'
host = 'https://s3.amazonaws.com'
eshost = 'https://vpc-petpair-vpc-vs3mfear47mid2ytzjvzc2kgj4.us-east-1.es.amazonaws.com'
index = 'pets'
type = 'Pet'
esurl = eshost + '/' + index + '/' + type + '/'


def lambda_handler(event, context):
    # TODO implement
    db.update_item(TableName='petpair-pet',
          Key={'pet_id':{'S':event['pet_id']}},
          AttributeUpdates={
                'name': {
                    'Value': {"S" : event['name']},
                    'Action': 'PUT'
                },
                'age': {
                    'Value': {"N" : event['age']},
                    'Action': 'PUT'
                },
                'gender': {
                    'Value': {"N" : event['gender']},
                    'Action': 'PUT'
                },
                'breed': {
                    'Value': {"S" : event['breed']},
                    'Action': 'PUT'
                },
                'description': {
                    'Value': {"S" : event['description']},
                    'Action': 'PUT'
                }
            }
          )
    if 'file' in event:
        file_name = event['pet_id'] + '.jpg'
        url = host + '/' + bucket + '/' + file_name
        file_content = base64.b64decode(event['file_content'])
        print(file_content)
        s3.put_object(ACL='public-read-write', Body=file_content, Bucket=bucket, Key=file_name)
        db.update_item(TableName='petpair-pet',
            Key={'pet_id':{'S':event['pet_id']}},
            AttributeUpdates={
                'pet_image': {
                    'Value': {"S" : url},
                    'Action': 'PUT'
                }
            }
        )
    # update to elastic search
    add_to_es(
        event['pet_id'],
        dict({
            "breed":event["breed"].lower(),
            "description":event["description"].lower()
            })
    )


    return {
        'statusCode': 200,
        'body': {}
    }

def add_to_es(id, data):
    region = 'us-east-1'  # e.g. us-east-1
    service = 'es'
    headers = {"Content-Type": "application/json"}
    r = requests.put(esurl + id, json=data, headers=headers)
    print(r)

