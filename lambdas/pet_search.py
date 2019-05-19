from __future__ import print_function
import requests
from requests_aws4auth import AWS4Auth
import time
from boto3.dynamodb.conditions import Key

import boto3
from decimal import Decimal
import json
import urllib

url = 'https://vpc-petparing-vpc-3fx4z2v6xqknlwatal3cwygtze.us-east-1.es.amazonaws.com/_search?size=50&'
s3 = boto3.client('s3')
db = boto3.resource('dynamodb')
pet_table = db.Table('petpair-pet')
user_table = db.Table('petpair-user')

def lambda_handler(event, context):
    # TODO: use lex to search
    to_search = event['query'].lower()
    user_email = event['user_email']
    tmp = user_table.query(KeyConditionExpression=Key('user_email').eq(user_email))
    keywords = set([str(k) for k in to_search.split(" ")])
    ans = dict({"Items":[]})
    ids = set()
    for k in keywords:
        dogs = json.loads(requests.get(url + "q=" + k).text)['hits']['hits']
        for dog in dogs:
            ids.add(dog['_id'])
    for id in ids:
        current_pet = pet_table.get_item(
            Key={
                "pet_id": id
            }
        )
        if current_pet['Item']['status'] != 0:
            continue;
        pet_id = current_pet['Item']['pet_id']
        if 'pets' in tmp['Items'][0] and len(tmp['Items']) > 0 and pet_id in tmp['Items'][0]['pets']:
            continue
        else:
            if len(tmp['Items']) > 0 and "wishlist" in tmp['Items'][0] and pet_id in tmp['Items'][0]['wishlist']:
                current_pet['Item']['like'] = '1'
            else:
                current_pet['Item']['like'] = '0'
            ans['Items'].append(current_pet['Item'])

    return {
        "statusCode": 200,
        "body": ans['Items'],
        "start_key": list(ids)[-1],
        "headers": {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
    }
}
