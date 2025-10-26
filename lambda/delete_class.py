import json
import boto3
import os

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
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'user_id and class_id are required'
                })
            }
        
        # Delete the item
        table.delete_item(
            Key={
                'user_id': user_id,
                'class_id': class_id
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Class deleted successfully',
                'class_id': class_id
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
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Failed to delete class',
                'error': str(e)
            })
        }
