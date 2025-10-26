import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['ASSIGNMENTS_TABLE_NAME'])

def lambda_handler(event, context):
    try:
        # Get user_id and assignment_id from path parameters
        path_params = event.get('pathParameters', {})
        user_id = path_params.get('user_id')
        assignment_id = path_params.get('assignment_id')
        
        if not user_id or not assignment_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({
                    'message': 'user_id and assignment_id are required'
                })
            }
        
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        # Build update expression
        update_expression_parts = []
        expression_attribute_values = {}
        expression_attribute_names = {}
        
        updatable_fields = ['title', 'description', 'class_id', 'class_name', 'due_date', 'status', 'notes']
        
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
                'assignment_id': assignment_id
            },
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues='ALL_NEW'
        )
        
        assignment = response['Attributes']
        
        # Format response
        formatted_assignment = {
            'id': assignment['assignment_id'],
            'title': assignment['title'],
            'description': assignment.get('description', ''),
            'class_id': assignment.get('class_id', ''),
            'class_name': assignment.get('class_name', ''),
            'due_date': assignment.get('due_date', ''),
            'status': assignment.get('status', 'pending'),
            'notes': assignment.get('notes', ''),
            'updated_at': timestamp
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(formatted_assignment)
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
                'message': 'Failed to update assignment',
                'error': str(e)
            })
        }
