import json
import boto3
import os
from datetime import datetime
import uuid
import base64

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table(os.environ['ASSIGNMENTS_TABLE_NAME'])
bucket_name = os.environ['S3_BUCKET_NAME']

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
        if 'title' not in body:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type'
                },
                'body': json.dumps({
                    'message': 'title is required'
                })
            }
        
        # Generate assignment ID
        assignment_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Create assignment item
        item = {
            'user_id': user_id,
            'assignment_id': assignment_id,
            'title': body['title'],
            'description': body.get('description', ''),
            'class_id': body.get('class_id', ''),
            'class_name': body.get('class_name', ''),
            'due_date': body.get('due_date', ''),
            'status': body.get('status', 'pending'),
            'notes': body.get('notes', ''),
            'created_at': timestamp,
            'updated_at': timestamp
        }
        
        # Handle file upload if provided
        if 'file_content' in body and 'file_name' in body:
            file_content = body['file_content']
            file_name = body['file_name']
            file_type = body.get('file_type', 'application/octet-stream')
            
            # Generate S3 key
            file_key = f"assignments/{user_id}/{assignment_id}/{file_name}"
            
            # Decode base64 if needed
            if body.get('file_encoding') == 'base64':
                file_content = base64.b64decode(file_content)
            elif isinstance(file_content, str):
                file_content = file_content.encode('utf-8')
            
            # Upload to S3
            s3.put_object(
                Bucket=bucket_name,
                Key=file_key,
                Body=file_content,
                ContentType=file_type
            )
            
            item['file_key'] = file_key
            item['file_name'] = file_name
            item['file_type'] = file_type
        
        # Save to DynamoDB
        table.put_item(Item=item)
        
        # Format response
        response_assignment = {
            'id': assignment_id,
            'title': item['title'],
            'description': item['description'],
            'class_id': item['class_id'],
            'class_name': item['class_name'],
            'due_date': item['due_date'],
            'status': item['status'],
            'created_at': timestamp
        }
        
        if 'file_key' in item:
            response_assignment['file_key'] = item['file_key']
            response_assignment['file_name'] = item['file_name']
            # Generate presigned URL
            url = s3.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': bucket_name,
                    'Key': item['file_key']
                },
                ExpiresIn=3600
            )
            response_assignment['file_url'] = url
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response_assignment)
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
                'message': 'Failed to create assignment',
                'error': str(e)
            })
        }
