output "api_id" {
  description = "API Gateway ID"
  value       = aws_apigatewayv2_api.chat_api.id
}

output "api_endpoint" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_stage.chat_api_stage.invoke_url
}

output "execution_arn" {
  description = "API Gateway execution ARN"
  value       = aws_apigatewayv2_api.chat_api.execution_arn
}

output "stage_name" {
  description = "API Gateway stage name"
  value       = aws_apigatewayv2_stage.chat_api_stage.name
}
