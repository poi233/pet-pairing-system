import json
import boto3

sqs = boto3.client('sqs')

def lambda_handler(event, context):
    # TODO implement
    from_email = event['from_email']
    to_email = event['to_email']
    sqs_message = from_email + "|" + to_email + "|" + event['content'];
    sqs.send_message(
        QueueUrl = 'https://sqs.us-east-1.amazonaws.com/007373548085/PetPairMessageQueue',
        MessageBody = sqs_message,
        DelaySeconds = 1
    )
    return {}