import json
import boto3
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        # Get user_id from query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        user_id = query_params.get('user_id')
        
        if not user_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'user_id query parameter is required'
                })
            }
        
        # Query chats for the user using GSI
        response = table.query(
            IndexName='user_id-updated_at-index',
            KeyConditionExpression=Key('user_id').eq(user_id),
            ScanIndexForward=False  # Sort in descending order (most recent first)
        )
        
        chats = response.get('Items', [])
        
        # Remove messages from list view for performance
        chats_summary = []
        for chat in chats:
            chat_summary = {
                'chat_id': chat['chat_id'],
                'user_id': chat['user_id'],
                'title': chat.get('title', 'Untitled Chat'),
                'created_at': chat['created_at'],
                'updated_at': chat['updated_at'],
                'message_count': len(chat.get('messages', []))
            }
            chats_summary.append(chat_summary)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'chats': chats_summary,
                'count': len(chats_summary)
            }, cls=DecimalEncoder)
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
                'message': 'Failed to list chats',
                'error': str(e)
            })
        }
