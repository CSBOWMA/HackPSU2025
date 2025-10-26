import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')
table = dynamodb.Table(os.environ['ASSIGNMENTS_TABLE_NAME'])
bucket_name = os.environ['S3_BUCKET_NAME']

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
        
        # Get assignment to find file_key
        response = table.get_item(
            Key={
                'user_id': user_id,
                'assignment_id': assignment_id
            }
        )
        
        # Delete file from S3 if exists
        if 'Item' in response and 'file_key' in response['Item']:
            try:
                s3.delete_object(
                    Bucket=bucket_name,
                    Key=response['Item']['file_key']
                )
            except Exception as e:
                print(f"Error deleting file from S3: {str(e)}")
        
        # Delete from DynamoDB
        table.delete_item(
            Key={
                'user_id': user_id,
                'assignment_id': assignment_id
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({
                'message': 'Assignment deleted successfully',
                'assignment_id': assignment_id
            })
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
                'message': 'Failed to delete assignment',
                'error': str(e)
            })
        }
