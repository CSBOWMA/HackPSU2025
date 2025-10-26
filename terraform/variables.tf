variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "project_name" {
  description = "Project name"
  type        = string
  default     = "chat-app"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}
