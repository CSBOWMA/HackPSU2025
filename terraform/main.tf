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

# DynamoDB Table with GSI for user_id queries
resource "aws_dynamodb_table" "chats_table" {
  name           = "${var.project_name}-${var.environment}-chats"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "chat_id"

  attribute {
    name = "chat_id"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "updated_at"
    type = "S"
  }

  global_secondary_index {
    name            = "user_id-updated_at-index"
    hash_key        = "user_id"
    range_key       = "updated_at"
    projection_type = "ALL"
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-chats"
    Environment = var.environment
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "${var.project_name}-${var.environment}-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for Lambda to access DynamoDB and Bedrock
resource "aws_iam_role_policy" "lambda_policy" {
  name = "${var.project_name}-${var.environment}-lambda-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:PutItem",
          "dynamodb:GetItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.chats_table.arn,
          "${aws_dynamodb_table.chats_table.arn}/index/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel"
        ]
        Resource = "arn:aws:bedrock:*::foundation-model/amazon.nova-lite-v1:0"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:*:*:*"
      }
    ]
  })
}

# API Gateway
resource "aws_apigatewayv2_api" "chat_api" {
  name          = "${var.project_name}-${var.environment}-api"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    allow_headers = ["*"]
  }
}

resource "aws_apigatewayv2_stage" "chat_api_stage" {
  api_id      = aws_apigatewayv2_api.chat_api.id
  name        = var.environment
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway_logs.arn
    format = jsonencode({
      requestId      = "$context.requestId"
      ip             = "$context.identity.sourceIp"
      requestTime    = "$context.requestTime"
      httpMethod     = "$context.httpMethod"
      routeKey       = "$context.routeKey"
      status         = "$context.status"
      protocol       = "$context.protocol"
      responseLength = "$context.responseLength"
    })
  }
}

resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "/aws/apigateway/${var.project_name}-${var.environment}"
  retention_in_days = 7
}

# Lambda: Create Chat
# Lambda: Create Chat
data "archive_file" "create_chat_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/create_chat.py"
  output_path = "${path.module}/../lambda/create_chat.zip"
}

resource "aws_lambda_function" "create_chat" {
  filename         = data.archive_file.create_chat_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-create-chat"
  role            = aws_iam_role.lambda_role.arn
  handler         = "create_chat.lambda_handler"
  source_code_hash = data.archive_file.create_chat_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.chats_table.name
      # Removed AWS_REGION - Lambda sets this automatically
    }
  }
}

resource "aws_cloudwatch_log_group" "create_chat_logs" {
  name              = "/aws/lambda/${aws_lambda_function.create_chat.function_name}"
  retention_in_days = 7
}

# Lambda: Get Chat
data "archive_file" "get_chat_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/get_chat.py"
  output_path = "${path.module}/../lambda/get_chat.zip"
}

resource "aws_lambda_function" "get_chat" {
  filename         = data.archive_file.get_chat_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-get-chat"
  role            = aws_iam_role.lambda_role.arn
  handler         = "get_chat.lambda_handler"
  source_code_hash = data.archive_file.get_chat_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.chats_table.name
    }
  }
}

resource "aws_cloudwatch_log_group" "get_chat_logs" {
  name              = "/aws/lambda/${aws_lambda_function.get_chat.function_name}"
  retention_in_days = 7
}

# Lambda: List Chats
data "archive_file" "list_chats_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/list_chats.py"
  output_path = "${path.module}/../lambda/list_chats.zip"
}

resource "aws_lambda_function" "list_chats" {
  filename         = data.archive_file.list_chats_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-list-chats"
  role            = aws_iam_role.lambda_role.arn
  handler         = "list_chats.lambda_handler"
  source_code_hash = data.archive_file.list_chats_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.chats_table.name
    }
  }
}

resource "aws_cloudwatch_log_group" "list_chats_logs" {
  name              = "/aws/lambda/${aws_lambda_function.list_chats.function_name}"
  retention_in_days = 7
}

# Lambda: Delete Chat
data "archive_file" "delete_chat_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/delete_chat.py"
  output_path = "${path.module}/../lambda/delete_chat.zip"
}

resource "aws_lambda_function" "delete_chat" {
  filename         = data.archive_file.delete_chat_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-delete-chat"
  role            = aws_iam_role.lambda_role.arn
  handler         = "delete_chat.lambda_handler"
  source_code_hash = data.archive_file.delete_chat_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.chats_table.name
    }
  }
}

resource "aws_cloudwatch_log_group" "delete_chat_logs" {
  name              = "/aws/lambda/${aws_lambda_function.delete_chat.function_name}"
  retention_in_days = 7
}

# Lambda: Append Message
data "archive_file" "append_message_zip" {
  type        = "zip"
  source_file = "${path.module}/../lambda/append_message.py"
  output_path = "${path.module}/../lambda/append_message.zip"
}

resource "aws_lambda_function" "append_message" {
  filename         = data.archive_file.append_message_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-append-message"
  role            = aws_iam_role.lambda_role.arn
  handler         = "append_message.lambda_handler"
  source_code_hash = data.archive_file.append_message_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.chats_table.name
    }
  }
}

resource "aws_cloudwatch_log_group" "append_message_logs" {
  name              = "/aws/lambda/${aws_lambda_function.append_message.function_name}"
  retention_in_days = 7
}

# Lambda Permissions for API Gateway
resource "aws_lambda_permission" "create_chat_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_chat.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.chat_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "get_chat_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_chat.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.chat_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "list_chats_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.list_chats.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.chat_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "delete_chat_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.delete_chat.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.chat_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "append_message_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.append_message.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.chat_api.execution_arn}/*/*"
}

# API Gateway Integrations
resource "aws_apigatewayv2_integration" "create_chat_integration" {
  api_id           = aws_apigatewayv2_api.chat_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.create_chat.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "get_chat_integration" {
  api_id           = aws_apigatewayv2_api.chat_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.get_chat.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "list_chats_integration" {
  api_id           = aws_apigatewayv2_api.chat_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.list_chats.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "delete_chat_integration" {
  api_id           = aws_apigatewayv2_api.chat_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.delete_chat.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "append_message_integration" {
  api_id           = aws_apigatewayv2_api.chat_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = aws_lambda_function.append_message.invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

# API Gateway Routes
resource "aws_apigatewayv2_route" "create_chat_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "POST /chats"
  target    = "integrations/${aws_apigatewayv2_integration.create_chat_integration.id}"
}

resource "aws_apigatewayv2_route" "get_chat_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "GET /chats/{chat_id}"
  target    = "integrations/${aws_apigatewayv2_integration.get_chat_integration.id}"
}

resource "aws_apigatewayv2_route" "list_chats_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "GET /chats"
  target    = "integrations/${aws_apigatewayv2_integration.list_chats_integration.id}"
}

resource "aws_apigatewayv2_route" "delete_chat_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "DELETE /chats/{chat_id}"
  target    = "integrations/${aws_apigatewayv2_integration.delete_chat_integration.id}"
}

resource "aws_apigatewayv2_route" "append_message_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "POST /chats/{chat_id}/messages"
  target    = "integrations/${aws_apigatewayv2_integration.append_message_integration.id}"
}
