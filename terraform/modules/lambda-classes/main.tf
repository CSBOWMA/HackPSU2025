# Lambda: Get All Classes
data "archive_file" "get_all_classes_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/get_all_classes.py"
  output_path = "${path.module}/../../../lambda/get_all_classes.zip"
}

resource "aws_lambda_function" "get_all_classes" {
  filename         = data.archive_file.get_all_classes_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-get-all-classes"
  role            = var.lambda_role_arn
  handler         = "get_all_classes.lambda_handler"
  source_code_hash = data.archive_file.get_all_classes_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      CLASSES_TABLE_NAME = var.classes_table_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-get-all-classes"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "get_all_classes_logs" {
  name              = "/aws/lambda/${aws_lambda_function.get_all_classes.function_name}"
  retention_in_days = 7
}

resource "aws_lambda_permission" "get_all_classes_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_all_classes.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Get Class By ID
data "archive_file" "get_class_by_id_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/get_class_by_id.py"
  output_path = "${path.module}/../../../lambda/get_class_by_id.zip"
}

resource "aws_lambda_function" "get_class_by_id" {
  filename         = data.archive_file.get_class_by_id_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-get-class-by-id"
  role            = var.lambda_role_arn
  handler         = "get_class_by_id.lambda_handler"
  source_code_hash = data.archive_file.get_class_by_id_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      CLASSES_TABLE_NAME = var.classes_table_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-get-class-by-id"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "get_class_by_id_logs" {
  name              = "/aws/lambda/${aws_lambda_function.get_class_by_id.function_name}"
  retention_in_days = 7
}

resource "aws_lambda_permission" "get_class_by_id_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_class_by_id.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Create Class
data "archive_file" "create_class_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/create_class.py"
  output_path = "${path.module}/../../../lambda/create_class.zip"
}

resource "aws_lambda_function" "create_class" {
  filename         = data.archive_file.create_class_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-create-class"
  role            = var.lambda_role_arn
  handler         = "create_class.lambda_handler"
  source_code_hash = data.archive_file.create_class_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      CLASSES_TABLE_NAME = var.classes_table_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-create-class"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "create_class_logs" {
  name              = "/aws/lambda/${aws_lambda_function.create_class.function_name}"
  retention_in_days = 7
}

resource "aws_lambda_permission" "create_class_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_class.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Update Class
data "archive_file" "update_class_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/update_class.py"
  output_path = "${path.module}/../../../lambda/update_class.zip"
}

resource "aws_lambda_function" "update_class" {
  filename         = data.archive_file.update_class_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-update-class"
  role            = var.lambda_role_arn
  handler         = "update_class.lambda_handler"
  source_code_hash = data.archive_file.update_class_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      CLASSES_TABLE_NAME = var.classes_table_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-update-class"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "update_class_logs" {
  name              = "/aws/lambda/${aws_lambda_function.update_class.function_name}"
  retention_in_days = 7
}

resource "aws_lambda_permission" "update_class_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_class.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Delete Class
data "archive_file" "delete_class_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/delete_class.py"
  output_path = "${path.module}/../../../lambda/delete_class.zip"
}

resource "aws_lambda_function" "delete_class" {
  filename         = data.archive_file.delete_class_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-delete-class"
  role            = var.lambda_role_arn
  handler         = "delete_class.lambda_handler"
  source_code_hash = data.archive_file.delete_class_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      CLASSES_TABLE_NAME = var.classes_table_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-delete-class"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "delete_class_logs" {
  name              = "/aws/lambda/${aws_lambda_function.delete_class.function_name}"
  retention_in_days = 7
}

resource "aws_lambda_permission" "delete_class_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.delete_class.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}
