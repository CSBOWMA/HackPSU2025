variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "lambda_role_name" {
  description = "Lambda IAM role name for S3 access"
  type        = string
}
