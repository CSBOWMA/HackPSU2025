terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

# DynamoDB Module (Chats)
module "dynamodb" {
  source = "./modules/dynamodb"

  project_name = var.project_name
  environment  = var.environment
}

# DynamoDB Module (Classes)
module "dynamodb_classes" {
  source = "./modules/dynamodb-classes"

  project_name = var.project_name
  environment  = var.environment
}

# DynamoDB Module (Assignments)
module "dynamodb_assignments" {
  source = "./modules/dynamodb-assignments"

  project_name = var.project_name
  environment  = var.environment
}

# IAM Module
module "iam" {
  source = "./modules/iam"

  project_name          = var.project_name
  environment           = var.environment
  dynamodb_table_arn    = module.dynamodb.table_arn
  dynamodb_gsi_arn      = module.dynamodb.gsi_arn
  classes_table_arn     = module.dynamodb_classes.table_arn
  classes_gsi_arn       = module.dynamodb_classes.gsi_arn
  assignments_table_arn = module.dynamodb_assignments.table_arn
  assignments_gsi_arn   = module.dynamodb_assignments.gsi_arn
}

# S3 Module
module "s3" {
  source = "./modules/s3"

  project_name     = var.project_name
  environment      = var.environment
  lambda_role_name = module.iam.lambda_role_name
}

# Lambda Module (Chats)
module "lambda" {
  source = "./modules/lambda"

  project_name        = var.project_name
  environment         = var.environment
  lambda_role_arn     = module.iam.lambda_role_arn
  dynamodb_table_name = module.dynamodb.table_name
  api_execution_arn   = module.api_gateway.execution_arn
}

# Lambda Module (Classes)
module "lambda_classes" {
  source = "./modules/lambda-classes"

  project_name        = var.project_name
  environment         = var.environment
  lambda_role_arn     = module.iam.lambda_role_arn
  classes_table_name  = module.dynamodb_classes.table_name
  api_execution_arn   = module.api_gateway.execution_arn
}

# Lambda Module (Assignments)
module "lambda_assignments" {
  source = "./modules/lambda-assignments"

  project_name           = var.project_name
  environment            = var.environment
  lambda_role_arn        = module.iam.lambda_role_arn
  assignments_table_name = module.dynamodb_assignments.table_name
  s3_bucket_name         = module.s3.bucket_name
  api_execution_arn      = module.api_gateway.execution_arn
}

# API Gateway Module
module "api_gateway" {
  source = "./modules/api-gateway"

  project_name = var.project_name
  environment  = var.environment

  # Chat Lambda function ARNs
  create_chat_invoke_arn    = module.lambda.create_chat_invoke_arn
  get_chat_invoke_arn       = module.lambda.get_chat_invoke_arn
  list_chats_invoke_arn     = module.lambda.list_chats_invoke_arn
  delete_chat_invoke_arn    = module.lambda.delete_chat_invoke_arn
  append_message_invoke_arn = module.lambda.append_message_invoke_arn

  # Chat Lambda function names
  create_chat_function_name    = module.lambda.create_chat_function_name
  get_chat_function_name       = module.lambda.get_chat_function_name
  list_chats_function_name     = module.lambda.list_chats_function_name
  delete_chat_function_name    = module.lambda.delete_chat_function_name
  append_message_function_name = module.lambda.append_message_function_name

  # Classes Lambda function ARNs
  get_all_classes_invoke_arn = module.lambda_classes.get_all_classes_invoke_arn
  get_class_by_id_invoke_arn = module.lambda_classes.get_class_by_id_invoke_arn
  create_class_invoke_arn    = module.lambda_classes.create_class_invoke_arn
  update_class_invoke_arn    = module.lambda_classes.update_class_invoke_arn
  delete_class_invoke_arn    = module.lambda_classes.delete_class_invoke_arn

  # Classes Lambda function names
  get_all_classes_function_name = module.lambda_classes.get_all_classes_function_name
  get_class_by_id_function_name = module.lambda_classes.get_class_by_id_function_name
  create_class_function_name    = module.lambda_classes.create_class_function_name
  update_class_function_name    = module.lambda_classes.update_class_function_name
  delete_class_function_name    = module.lambda_classes.delete_class_function_name

  # Assignments Lambda function ARNs
  list_assignments_invoke_arn  = module.lambda_assignments.list_assignments_invoke_arn
  get_assignment_invoke_arn    = module.lambda_assignments.get_assignment_invoke_arn
  create_assignment_invoke_arn = module.lambda_assignments.create_assignment_invoke_arn
  update_assignment_invoke_arn = module.lambda_assignments.update_assignment_invoke_arn
  delete_assignment_invoke_arn = module.lambda_assignments.delete_assignment_invoke_arn

  # Assignments Lambda function names
  list_assignments_function_name  = module.lambda_assignments.list_assignments_function_name
  get_assignment_function_name    = module.lambda_assignments.get_assignment_function_name
  create_assignment_function_name = module.lambda_assignments.create_assignment_function_name
  update_assignment_function_name = module.lambda_assignments.update_assignment_function_name
  delete_assignment_function_name = module.lambda_assignments.delete_assignment_function_name
}
