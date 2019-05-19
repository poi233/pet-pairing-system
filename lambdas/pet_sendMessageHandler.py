import json
import boto3

ses = boto3.client('ses')
sqs = boto3.client('sqs')
queue_url = 'https://sqs.us-east-1.amazonaws.com/007373548085/PetPairMessageQueue'

def lambda_handler(event, context):
    messages = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=10,
    )
    if 'Messages' in messages:
        for message in messages['Messages']:
            from_email = message['Body'].split("|")[0]
            to_email = message['Body'].split("|")[1]
            content = message['Body'].split("|")[2]
            receipt_handle = message['ReceiptHandle']
            sqs.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )

            response = ses.send_email(
                Source=from_email,
                Destination={
                    'ToAddresses': [to_email],
                },
                Message={
                    'Subject': {
                        'Data': "I like your dog",
                    },
                    'Body': {
                        'Text': {
                            'Data': content + " from " + from_email,
                        }
                    }
                })
    return {}
