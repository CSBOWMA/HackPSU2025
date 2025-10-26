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

variable "assignments_table_name" {
  description = "DynamoDB assignments table name"
  type        = string
}

variable "s3_bucket_name" {
  description = "S3 bucket name for assignment files"
  type        = string
}

variable "api_execution_arn" {
  description = "API Gateway execution ARN"
  type        = string
}
