output "get_all_classes_function_name" {
  description = "Get All Classes Lambda function name"
  value       = aws_lambda_function.get_all_classes.function_name
}

output "get_all_classes_invoke_arn" {
  description = "Get All Classes Lambda invoke ARN"
  value       = aws_lambda_function.get_all_classes.invoke_arn
}

output "get_class_by_id_function_name" {
  description = "Get Class By ID Lambda function name"
  value       = aws_lambda_function.get_class_by_id.function_name
}

output "get_class_by_id_invoke_arn" {
  description = "Get Class By ID Lambda invoke ARN"
  value       = aws_lambda_function.get_class_by_id.invoke_arn
}

output "create_class_function_name" {
  description = "Create Class Lambda function name"
  value       = aws_lambda_function.create_class.function_name
}

output "create_class_invoke_arn" {
  description = "Create Class Lambda invoke ARN"
  value       = aws_lambda_function.create_class.invoke_arn
}

output "update_class_function_name" {
  description = "Update Class Lambda function name"
  value       = aws_lambda_function.update_class.function_name
}

output "update_class_invoke_arn" {
  description = "Update Class Lambda invoke ARN"
  value       = aws_lambda_function.update_class.invoke_arn
}

output "delete_class_function_name" {
  description = "Delete Class Lambda function name"
  value       = aws_lambda_function.delete_class.function_name
}

output "delete_class_invoke_arn" {
  description = "Delete Class Lambda invoke ARN"
  value       = aws_lambda_function.delete_class.invoke_arn
}
