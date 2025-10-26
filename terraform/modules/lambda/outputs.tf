output "create_chat_function_name" {
  description = "Create Chat Lambda function name"
  value       = aws_lambda_function.create_chat.function_name
}

output "create_chat_invoke_arn" {
  description = "Create Chat Lambda invoke ARN"
  value       = aws_lambda_function.create_chat.invoke_arn
}

output "get_chat_function_name" {
  description = "Get Chat Lambda function name"
  value       = aws_lambda_function.get_chat.function_name
}

output "get_chat_invoke_arn" {
  description = "Get Chat Lambda invoke ARN"
  value       = aws_lambda_function.get_chat.invoke_arn
}

output "list_chats_function_name" {
  description = "List Chats Lambda function name"
  value       = aws_lambda_function.list_chats.function_name
}

output "list_chats_invoke_arn" {
  description = "List Chats Lambda invoke ARN"
  value       = aws_lambda_function.list_chats.invoke_arn
}

output "delete_chat_function_name" {
  description = "Delete Chat Lambda function name"
  value       = aws_lambda_function.delete_chat.function_name
}

output "delete_chat_invoke_arn" {
  description = "Delete Chat Lambda invoke ARN"
  value       = aws_lambda_function.delete_chat.invoke_arn
}

output "append_message_function_name" {
  description = "Append Message Lambda function name"
  value       = aws_lambda_function.append_message.function_name
}

output "append_message_invoke_arn" {
  description = "Append Message Lambda invoke ARN"
  value       = aws_lambda_function.append_message.invoke_arn
}
