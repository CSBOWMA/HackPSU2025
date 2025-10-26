output "list_assignments_function_name" {
  description = "List Assignments Lambda function name"
  value       = aws_lambda_function.list_assignments.function_name
}

output "list_assignments_invoke_arn" {
  description = "List Assignments Lambda invoke ARN"
  value       = aws_lambda_function.list_assignments.invoke_arn
}

output "get_assignment_function_name" {
  description = "Get Assignment Lambda function name"
  value       = aws_lambda_function.get_assignment.function_name
}

output "get_assignment_invoke_arn" {
  description = "Get Assignment Lambda invoke ARN"
  value       = aws_lambda_function.get_assignment.invoke_arn
}

output "create_assignment_function_name" {
  description = "Create Assignment Lambda function name"
  value       = aws_lambda_function.create_assignment.function_name
}

output "create_assignment_invoke_arn" {
  description = "Create Assignment Lambda invoke ARN"
  value       = aws_lambda_function.create_assignment.invoke_arn
}

output "update_assignment_function_name" {
  description = "Update Assignment Lambda function name"
  value       = aws_lambda_function.update_assignment.function_name
}

output "update_assignment_invoke_arn" {
  description = "Update Assignment Lambda invoke ARN"
  value       = aws_lambda_function.update_assignment.invoke_arn
}

output "delete_assignment_function_name" {
  description = "Delete Assignment Lambda function name"
  value       = aws_lambda_function.delete_assignment.function_name
}

output "delete_assignment_invoke_arn" {
  description = "Delete Assignment Lambda invoke ARN"
  value       = aws_lambda_function.delete_assignment.invoke_arn
}
