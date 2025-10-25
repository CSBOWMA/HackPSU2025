output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_stage.chat_api_stage.invoke_url
}

output "dynamodb_table_name" {
  description = "DynamoDB table name"
  value       = aws_dynamodb_table.chats_table.name
}

output "create_chat_function_name" {
  description = "Create Chat Lambda function name"
  value       = aws_lambda_function.create_chat.function_name
}

output "get_chat_function_name" {
  description = "Get Chat Lambda function name"
  value       = aws_lambda_function.get_chat.function_name
}

output "list_chats_function_name" {
  description = "List Chats Lambda function name"
  value       = aws_lambda_function.list_chats.function_name
}

output "delete_chat_function_name" {
  description = "Delete Chat Lambda function name"
  value       = aws_lambda_function.delete_chat.function_name
}

output "append_message_function_name" {
  description = "Append Message Lambda function name"
  value       = aws_lambda_function.append_message.function_name
}

output "api_routes" {
  description = "Available API routes"
  value = {
    create_chat    = "POST ${aws_apigatewayv2_stage.chat_api_stage.invoke_url}/chats"
    get_chat       = "GET ${aws_apigatewayv2_stage.chat_api_stage.invoke_url}/chats/{chat_id}"
    list_chats     = "GET ${aws_apigatewayv2_stage.chat_api_stage.invoke_url}/chats?user_id={user_id}"
    delete_chat    = "DELETE ${aws_apigatewayv2_stage.chat_api_stage.invoke_url}/chats/{chat_id}"
    append_message = "POST ${aws_apigatewayv2_stage.chat_api_stage.invoke_url}/chats/{chat_id}/messages"
  }
}
