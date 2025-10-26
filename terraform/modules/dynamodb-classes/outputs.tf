output "table_name" {
  description = "DynamoDB classes table name"
  value       = aws_dynamodb_table.classes_table.name
}

output "table_arn" {
  description = "DynamoDB classes table ARN"
  value       = aws_dynamodb_table.classes_table.arn
}

output "gsi_arn" {
  description = "DynamoDB classes GSI ARN"
  value       = "${aws_dynamodb_table.classes_table.arn}/index/*"
}
