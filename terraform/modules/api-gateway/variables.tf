variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

# Chat Lambda variables
variable "create_chat_invoke_arn" {
  description = "Create Chat Lambda invoke ARN"
  type        = string
}

variable "get_chat_invoke_arn" {
  description = "Get Chat Lambda invoke ARN"
  type        = string
}

variable "list_chats_invoke_arn" {
  description = "List Chats Lambda invoke ARN"
  type        = string
}

variable "delete_chat_invoke_arn" {
  description = "Delete Chat Lambda invoke ARN"
  type        = string
}

variable "append_message_invoke_arn" {
  description = "Append Message Lambda invoke ARN"
  type        = string
}

variable "create_chat_function_name" {
  description = "Create Chat Lambda function name"
  type        = string
}

variable "get_chat_function_name" {
  description = "Get Chat Lambda function name"
  type        = string
}

variable "list_chats_function_name" {
  description = "List Chats Lambda function name"
  type        = string
}

variable "delete_chat_function_name" {
  description = "Delete Chat Lambda function name"
  type        = string
}

variable "append_message_function_name" {
  description = "Append Message Lambda function name"
  type        = string
}

# Classes Lambda variables
variable "get_all_classes_invoke_arn" {
  description = "Get All Classes Lambda invoke ARN"
  type        = string
}

variable "get_class_by_id_invoke_arn" {
  description = "Get Class By ID Lambda invoke ARN"
  type        = string
}

variable "create_class_invoke_arn" {
  description = "Create Class Lambda invoke ARN"
  type        = string
}

variable "update_class_invoke_arn" {
  description = "Update Class Lambda invoke ARN"
  type        = string
}

variable "delete_class_invoke_arn" {
  description = "Delete Class Lambda invoke ARN"
  type        = string
}

variable "get_all_classes_function_name" {
  description = "Get All Classes Lambda function name"
  type        = string
}

variable "get_class_by_id_function_name" {
  description = "Get Class By ID Lambda function name"
  type        = string
}

variable "create_class_function_name" {
  description = "Create Class Lambda function name"
  type        = string
}

variable "update_class_function_name" {
  description = "Update Class Lambda function name"
  type        = string
}

variable "delete_class_function_name" {
  description = "Delete Class Lambda function name"
  type        = string
}
