output "table_name" {
  description = "DynamoDB table name"
  value       = aws_dynamodb_table.chats_table.name
}

output "table_arn" {
  description = "DynamoDB table ARN"
  value       = aws_dynamodb_table.chats_table.arn
}

output "gsi_arn" {
  description = "DynamoDB GSI ARN"
  value       = "${aws_dynamodb_table.chats_table.arn}/index/*"
}
