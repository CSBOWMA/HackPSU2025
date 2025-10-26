variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "lambda_role_arn" {
  description = "Lambda IAM role ARN"
  type        = string
}

variable "classes_table_name" {
  description = "DynamoDB classes table name"
  type        = string
}

variable "api_execution_arn" {
  description = "API Gateway execution ARN"
    type = string
}
