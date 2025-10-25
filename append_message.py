import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    try:
        # Get chat_id from path parameters
        chat_id = event.get('pathParameters', {}).get('chat_id')
        
        if not chat_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'chat_id is required'
                })
            }
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        message = body.get('message')
        role = body.get('role', 'user')
        
        if not message:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'message is required'
                })
            }
        
        timestamp = datetime.utcnow().isoformat()
        
        # Create message object
        new_message = {
            'role': role,
            'content': message,
            'timestamp': timestamp
        }
        
        # Append message to the messages list
        response = table.update_item(
            Key={'chat_id': chat_id},
            UpdateExpression='SET messages = list_append(if_not_exists(messages, :empty_list), :new_message), updated_at = :updated_at',
            ExpressionAttributeValues={
                ':new_message': [new_message],
                ':empty_list': [],
                ':updated_at': timestamp
            },
            ReturnValues='ALL_NEW'
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Message appended successfully',
                'chat_id': chat_id,
                'updated_at': timestamp,
                'total_messages': len(response['Attributes']['messages'])
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Failed to append message',
                'error': str(e)
            })
        }
