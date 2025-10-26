import json
import boto3
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CLASSES_TABLE_NAME'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

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
        
        # Query all classes for the user
        response = table.query(
            KeyConditionExpression=Key('user_id').eq(user_id)
        )
        
        classes = response.get('Items', [])
        
        # Transform to match frontend interface
        formatted_classes = []
        for cls in classes:
            formatted_class = {
                'id': cls['class_id'],
                'name': cls['name'],
                'code': cls['code'],
                'instructor': cls['instructor'],
                'schedule': cls['schedule'],
                'semester': cls['semester']
            }
            
            # Add optional fields if they exist
            if 'color' in cls:
                formatted_class['color'] = cls['color']
            if 'description' in cls:
                formatted_class['description'] = cls['description']
            
            formatted_classes.append(formatted_class)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'classes': formatted_classes
            }, cls=DecimalEncoder)
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
                'message': 'Failed to get classes',
                'error': str(e)
            })
        }
