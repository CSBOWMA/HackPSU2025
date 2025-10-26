output "table_name" {
  description = "DynamoDB assignments table name"
  value       = aws_dynamodb_table.assignments_table.name
}

output "table_arn" {
  description = "DynamoDB assignments table ARN"
  value       = aws_dynamodb_table.assignments_table.arn
}

output "gsi_arn" {
  description = "DynamoDB assignments GSI ARN"
  value       = "${aws_dynamodb_table.assignments_table.arn}/index/*"
}
