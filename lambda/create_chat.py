import json
import boto3
import os
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def generate_title(first_message):
    """Generate a short title from the first message using Amazon Nova"""
    try:
        # Use the AWS_DEFAULT_REGION environment variable that Lambda sets automatically
        region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-2')
        bedrock = boto3.client('bedrock-runtime', region_name=region)
        
        prompt = f"""Generate a short, concise title (maximum 6 words) that summarizes this message. 
Only return the title, nothing else.

Message: {first_message}

Title:"""

        # Amazon Nova Lite API format
        request_body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "inferenceConfig": {
                "max_new_tokens": 50,
                "temperature": 0.7
            }
        }
        
        response = bedrock.invoke_model(
            modelId='amazon.nova-lite-v1:0',
            contentType='application/json',
            accept='application/json',
            body=json.dumps(request_body)
        )
        
        response_body = json.loads(response['body'].read())
        
        # Amazon Nova response format
        title = response_body['output']['message']['content'][0]['text'].strip()
        
        # Remove quotes if present
        title = title.strip('"').strip("'")
        
        # Truncate if too long
        if len(title) > 60:
            title = title[:57] + "..."
            
        return title
        
    except Exception as e:
        print(f"Error generating title: {str(e)}")
        import traceback
        traceback.print_exc()
        # Fallback to first few words of message
        words = first_message.split()[:6]
        return ' '.join(words) + ('...' if len(first_message.split()) > 6 else '')

def lambda_handler(event, context):
    try:
        # Parse request body
        body = json.loads(event.get('body', '{}'))
        
        first_message = body.get('message')
        role = body.get('role', 'user')
        user_id = body.get('user_id')
        
        if not first_message:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'message is required'
                })
            }
        
        if not user_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'message': 'user_id is required'
                })
            }
        
        chat_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        
        # Generate title from first message
        title = generate_title(first_message)
        
        # Create message object
        message_obj = {
            'role': role,
            'content': first_message,
            'timestamp': timestamp
        }
        
        # Create new chat item
        item = {
            'chat_id': chat_id,
            'user_id': user_id,
            'title': title,
            'created_at': timestamp,
            'updated_at': timestamp,
            'messages': [message_obj],
            'metadata': body.get('metadata', {})
        }
        
        # Put item in DynamoDB
        table.put_item(Item=item)
        
        return {
            'statusCode': 201,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'message': 'Chat created successfully',
                'chat_id': chat_id,
                'title': title,
                'created_at': timestamp,
                'user_id': user_id
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
                'message': 'Failed to create chat',
                'error': str(e)
            })
        }
