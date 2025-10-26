import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['CLASSES_TABLE_NAME'])

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
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({
                    'message': 'user_id and class_id are required'
                })
            }
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Build update expression
        update_expression_parts = []
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        # Fields that can be updated
        updatable_fields = ['name', 'code', 'instructor', 'schedule', 'semester', 'color', 'description']
        
        for field in updatable_fields:
            if field in body:
                update_expression_parts.append(f"#{field} = :{field}")
                expression_attribute_values[f":{field}"] = body[field]
                expression_attribute_names[f"#{field}"] = field
        
        if not update_expression_parts:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({
                    'message': 'No fields to update'
                })
            }
        
        # Add updated_at timestamp
        timestamp = datetime.utcnow().isoformat()
        update_expression_parts.append("#updated_at = :updated_at")
        expression_attribute_values[":updated_at"] = timestamp
        expression_attribute_names["#updated_at"] = "updated_at"
        
        update_expression = "SET " + ", ".join(update_expression_parts)
        
        # Update the item
        response = table.update_item(
            Key={
                'user_id': user_id,
                'class_id': class_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues='ALL_NEW'
        )
        
        cls = response['Attributes']
        
        # Transform to match frontend interface
        formatted_class = {
            'id': cls['class_id'],
            'name': cls['name'],
            'code': cls['code'],
            'instructor': cls['instructor'],
            'schedule': cls['schedule'],
            'semester': cls['semester']
        }
        
        if 'color' in cls:
            formatted_class['color'] = cls['color']
        if 'description' in cls:
            formatted_class['description'] = cls['description']
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(formatted_class)
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
                'message': 'Failed to update class',
                'error': str(e)
            })
        }
