import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CLASSES_TABLE_NAME'])

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        # Get user_id and class_id from path parameters
        path_params = event.get('pathParameters', {})
        user_id = path_params.get('user_id')
        class_id = path_params.get('class_id')
        
        if not user_id or not class_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'user_id and class_id are required'
                })
            }
        
        # Get the class from DynamoDB
        response = table.get_item(
            Key={
                'user_id': user_id,
                'class_id': class_id
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'Class not found'
                })
            }
        
        cls = response['Item']
        
        # Transform to match frontend interface
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
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(formatted_class, cls=DecimalEncoder)
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Failed to get class',
                'error': str(e)
            })
        }
