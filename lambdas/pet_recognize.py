import json
import boto3
import base64

rekognition = boto3.client('rekognition')


def lambda_handler(event, context):
    # TODO implement
    exclude = ['dog', 'mammal', 'animal', 'pet', 'human', 'person']
    file_content = base64.b64decode(event['file_content'])
    response = rekognition.detect_labels(Image={"Bytes":file_content})
    for label in response['Labels']:
        if label['Name'].lower() not in exclude:
            return {'label': label['Name']}
    return {'label': ""}