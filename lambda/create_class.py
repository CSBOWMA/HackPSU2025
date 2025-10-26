import json
import boto3
import os
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CLASSES_TABLE_NAME'])

def lambda_handler(event, context):
    try:
        # Get user_id from path parameters
        user_id = event.get('pathParameters', {}).get('user_id')
        
        if not user_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({
                    'message': 'user_id is required'
                })
            }
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Validate required fields
        required_fields = ['name', 'code', 'instructor', 'schedule', 'semester']
        for field in required_fields:
            if field not in body:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                        'Access-Control-Allow-Headers': 'Content-Type'
                    },
                    'body': json.dumps({
                        'message': f'{field} is required'
                    })
                }
        
        # Generate class ID
        class_id = body.get('id', str(uuid.uuid4()))
        timestamp = datetime.utcnow().isoformat()
        
        # Create class item
        item = {
            'user_id': user_id,
            'class_id': class_id,
            'name': body['name'],
            'code': body['code'],
            'instructor': body['instructor'],
            'schedule': body['schedule'],
            'semester': body['semester'],
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        # Add optional fields
        if 'color' in body:
            item['color'] = body['color']
        if 'description' in body:
            item['description'] = body['description']
        
        # Put item in DynamoDB
        table.put_item(Item=item)
        
        # Return formatted response
        response_class = {
            'id': class_id,
            'name': item['name'],
            'code': item['code'],
            'instructor': item['instructor'],
            'schedule': item['schedule'],
            'semester': item['semester']
        }
        
        if 'color' in item:
            response_class['color'] = item['color']
        if 'description' in item:
            response_class['description'] = item['description']
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response_class)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'message': 'Failed to create class',
                'error': str(e)
            })
        }
