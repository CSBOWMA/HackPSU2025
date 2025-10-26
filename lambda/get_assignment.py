import json
import boto3
import os
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table(os.environ['ASSIGNMENTS_TABLE_NAME'])
bucket_name = os.environ['S3_BUCKET_NAME']

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

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
        
        # Get assignment from DynamoDB
        response = table.get_item(
            Key={
                'user_id': user_id,
                'assignment_id': assignment_id
            }
        )
        
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({
                    'message': 'Assignment not found'
                })
            }
        
        assignment = response['Item']
        
        # Format assignment
        formatted_assignment = {
            'id': assignment['assignment_id'],
            'title': assignment['title'],
            'description': assignment.get('description', ''),
            'class_id': assignment.get('class_id', ''),
            'class_name': assignment.get('class_name', ''),
            'due_date': assignment.get('due_date', ''),
            'status': assignment.get('status', 'pending'),
            'file_key': assignment.get('file_key', ''),
            'file_name': assignment.get('file_name', ''),
            'file_type': assignment.get('file_type', ''),
            'created_at': assignment.get('created_at', ''),
            'updated_at': assignment.get('updated_at', ''),
            'notes': assignment.get('notes', '')
        }
        
        # Generate presigned URL for file if exists
        if assignment.get('file_key'):
            try:
                url = s3.generate_presigned_url(
                    'get_object',
                    Params={
                        'Bucket': bucket_name,
                        'Key': assignment['file_key']
                    },
                    ExpiresIn=3600
                )
                formatted_assignment['file_url'] = url
            except Exception as e:
                print(f"Error generating presigned URL: {str(e)}")
                formatted_assignment['file_url'] = None
        
        # If file is text-based, optionally read content
        if assignment.get('file_type') in ['text/plain', 'text/markdown', 'application/json']:
            try:
                obj = s3.get_object(Bucket=bucket_name, Key=assignment['file_key'])
                content = obj['Body'].read().decode('utf-8')
                formatted_assignment['file_content'] = content
            except Exception as e:
                print(f"Error reading file content: {str(e)}")
                formatted_assignment['file_content'] = None
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(formatted_assignment, cls=DecimalEncoder)
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
                'message': 'Failed to get assignment',
                'error': str(e)
            })
        }
