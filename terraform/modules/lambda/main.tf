# Lambda: Create Chat
data "archive_file" "create_chat_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/create_chat.py"
  output_path = "${path.module}/../../../lambda/create_chat.zip"
}

resource "aws_lambda_function" "create_chat" {
  filename         = data.archive_file.create_chat_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-create-chat"
  role            = var.lambda_role_arn
  handler         = "create_chat.lambda_handler"
  source_code_hash = data.archive_file.create_chat_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-create-chat"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "create_chat_logs" {
  name              = "/aws/lambda/${aws_lambda_function.create_chat.function_name}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "create_chat_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_chat.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Get Chat
data "archive_file" "get_chat_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/get_chat.py"
  output_path = "${path.module}/../../../lambda/get_chat.zip"
}

resource "aws_lambda_function" "get_chat" {
  filename         = data.archive_file.get_chat_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-get-chat"
  role            = var.lambda_role_arn
  handler         = "get_chat.lambda_handler"
  source_code_hash = data.archive_file.get_chat_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-get-chat"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "get_chat_logs" {
  name              = "/aws/lambda/${aws_lambda_function.get_chat.function_name}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "get_chat_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_chat.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: List Chats
data "archive_file" "list_chats_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/list_chats.py"
  output_path = "${path.module}/../../../lambda/list_chats.zip"
}

resource "aws_lambda_function" "list_chats" {
  filename         = data.archive_file.list_chats_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-list-chats"
  role            = var.lambda_role_arn
  handler         = "list_chats.lambda_handler"
  source_code_hash = data.archive_file.list_chats_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-list-chats"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "list_chats_logs" {
  name              = "/aws/lambda/${aws_lambda_function.list_chats.function_name}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "list_chats_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.list_chats.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Delete Chat
data "archive_file" "delete_chat_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/delete_chat.py"
  output_path = "${path.module}/../../../lambda/delete_chat.zip"
}

resource "aws_lambda_function" "delete_chat" {
  filename         = data.archive_file.delete_chat_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-delete-chat"
  role            = var.lambda_role_arn
  handler         = "delete_chat.lambda_handler"
  source_code_hash = data.archive_file.delete_chat_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-delete-chat"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "delete_chat_logs" {
  name              = "/aws/lambda/${aws_lambda_function.delete_chat.function_name}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "delete_chat_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.delete_chat.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Append Message
data "archive_file" "append_message_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/append_message.py"
  output_path = "${path.module}/../../../lambda/append_message.zip"
}

resource "aws_lambda_function" "append_message" {
  filename         = data.archive_file.append_message_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-append-message"
  role            = var.lambda_role_arn
  handler         = "append_message.lambda_handler"
  source_code_hash = data.archive_file.append_message_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      TABLE_NAME = var.dynamodb_table_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-append-message"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "append_message_logs" {
  name              = "/aws/lambda/${aws_lambda_function.append_message.function_name}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "append_message_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.append_message.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}
