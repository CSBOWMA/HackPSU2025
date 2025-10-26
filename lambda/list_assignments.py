import json
import boto3
import os
from decimal import Decimal
from boto3.dynamodb.conditions import Key

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
        # Get user_id from path parameters
        user_id = event.get('pathParameters', {}).get('user_id')
        
        # Get optional query parameters
        query_params = event.get('queryStringParameters', {}) or {}
        class_id = query_params.get('class_id')
        
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
        
        # Query assignments - filter by class if provided
        if class_id:
            response = table.query(
                IndexName='user_id-class_id-index',
                KeyConditionExpression=Key('user_id').eq(user_id) & Key('class_id').eq(class_id)
            )
        else:
            response = table.query(
                KeyConditionExpression=Key('user_id').eq(user_id)
            )
        
        assignments = response.get('Items', [])
        
        # Format assignments
        formatted_assignments = []
        for assignment in assignments:
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
                'updated_at': assignment.get('updated_at', '')
            }
            
            # Add file URL if file exists
            if assignment.get('file_key'):
                # Generate presigned URL (valid for 1 hour)
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
            
            formatted_assignments.append(formatted_assignment)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'assignments': formatted_assignments,
                'count': len(formatted_assignments)
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
                'message': 'Failed to list assignments',
                'error': str(e)
            })
        }
