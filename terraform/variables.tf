# variables.tf

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "chat-app"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "use_dynamodb" {
  description = "Whether to create DynamoDB resources and permissions"
  type        = bool
  default     = true
}

variable "use_lambda" {
  description = "Whether to create Lambda invoke permissions"
  type        = bool
  default     = false
}
