variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "dynamodb_table_arn" {
  description = "DynamoDB table ARN"
  type        = string
}

variable "dynamodb_gsi_arn" {
  description = "DynamoDB GSI ARN"
  type        = string
}

variable "classes_table_arn" {
  description = "DynamoDB classes table ARN"
  type        = string
}

variable "classes_gsi_arn" {
  description = "DynamoDB classes GSI ARN"
  type        = string
}

variable "assignments_table_arn" {
  description = "DynamoDB assignments table ARN"
  type        = string
}

variable "assignments_gsi_arn" {
  description = "DynamoDB assignments GSI ARN"
  type        = string
}
