output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = module.api_gateway.api_endpoint
}

output "api_id" {
  description = "API Gateway ID"
  value       = module.api_gateway.api_id
}

output "dynamodb_chats_table_name" {
  description = "DynamoDB chats table name"
  value       = module.dynamodb.table_name
}

output "dynamodb_classes_table_name" {
  description = "DynamoDB classes table name"
  value       = module.dynamodb_classes.table_name
}

output "s3_bucket_name" {
  description = "S3 bucket name for RAG data"
  value       = module.s3.bucket_name
}

output "s3_user_name" {
  description = "IAM user name for S3 access"
  value       = module.s3.iam_user_name
}

output "s3_access_key_id" {
  description = "AWS Access Key ID for S3 user"
  value       = module.s3.access_key_id
}

output "s3_secret_access_key" {
  description = "AWS Secret Access Key for S3 user (sensitive)"
  value       = module.s3.secret_access_key
  sensitive   = true
}

output "lambda_function_names" {
  description = "Lambda function names"
  value = {
    # Chat functions
    create_chat    = module.lambda.create_chat_function_name
    get_chat       = module.lambda.get_chat_function_name
    list_chats     = module.lambda.list_chats_function_name
    delete_chat    = module.lambda.delete_chat_function_name
    append_message = module.lambda.append_message_function_name
    
    # Classes functions
    get_all_classes = module.lambda_classes.get_all_classes_function_name
    get_class_by_id = module.lambda_classes.get_class_by_id_function_name
    create_class    = module.lambda_classes.create_class_function_name
    update_class    = module.lambda_classes.update_class_function_name
    delete_class    = module.lambda_classes.delete_class_function_name
  }
}

output "api_routes" {
  description = "Available API routes"
  value = {
    # Chat routes
    create_chat    = "POST ${module.api_gateway.api_endpoint}/chats"
    get_chat       = "GET ${module.api_gateway.api_endpoint}/chats/{chat_id}"
    list_chats     = "GET ${module.api_gateway.api_endpoint}/chats?user_id={user_id}"
    delete_chat    = "DELETE ${module.api_gateway.api_endpoint}/chats/{chat_id}"
    append_message = "POST ${module.api_gateway.api_endpoint}/chats/{chat_id}/messages"
    
    # Classes routes
    get_all_classes = "GET ${module.api_gateway.api_endpoint}/users/{user_id}/classes"
    get_class_by_id = "GET ${module.api_gateway.api_endpoint}/users/{user_id}/classes/{class_id}"
    create_class    = "POST ${module.api_gateway.api_endpoint}/users/{user_id}/classes"
    update_class    = "PUT ${module.api_gateway.api_endpoint}/users/{user_id}/classes/{class_id}"
    delete_class    = "DELETE ${module.api_gateway.api_endpoint}/users/{user_id}/classes/{class_id}"
  }
}
