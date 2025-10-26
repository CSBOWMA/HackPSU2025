# Lambda: List Assignments
data "archive_file" "list_assignments_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/list_assignments.py"
  output_path = "${path.module}/../../../lambda/list_assignments.zip"
}

resource "aws_lambda_function" "list_assignments" {
  filename         = data.archive_file.list_assignments_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-list-assignments"
  role            = var.lambda_role_arn
  handler         = "list_assignments.lambda_handler"
  source_code_hash = data.archive_file.list_assignments_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      ASSIGNMENTS_TABLE_NAME = var.assignments_table_name
      S3_BUCKET_NAME        = var.s3_bucket_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-list-assignments"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "list_assignments_logs" {
  name              = "/aws/lambda/${aws_lambda_function.list_assignments.function_name}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "list_assignments_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.list_assignments.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Get Assignment
data "archive_file" "get_assignment_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/get_assignment.py"
  output_path = "${path.module}/../../../lambda/get_assignment.zip"
}

resource "aws_lambda_function" "get_assignment" {
  filename         = data.archive_file.get_assignment_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-get-assignment"
  role            = var.lambda_role_arn
  handler         = "get_assignment.lambda_handler"
  source_code_hash = data.archive_file.get_assignment_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      ASSIGNMENTS_TABLE_NAME = var.assignments_table_name
      S3_BUCKET_NAME        = var.s3_bucket_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-get-assignment"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "get_assignment_logs" {
  name              = "/aws/lambda/${aws_lambda_function.get_assignment.function_name}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "get_assignment_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.get_assignment.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Create Assignment
data "archive_file" "create_assignment_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/create_assignment.py"
  output_path = "${path.module}/../../../lambda/create_assignment.zip"
}

resource "aws_lambda_function" "create_assignment" {
  filename         = data.archive_file.create_assignment_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-create-assignment"
  role            = var.lambda_role_arn
  handler         = "create_assignment.lambda_handler"
  source_code_hash = data.archive_file.create_assignment_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      ASSIGNMENTS_TABLE_NAME = var.assignments_table_name
      S3_BUCKET_NAME        = var.s3_bucket_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-create-assignment"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "create_assignment_logs" {
  name              = "/aws/lambda/${aws_lambda_function.create_assignment.function_name}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "create_assignment_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_assignment.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Update Assignment
data "archive_file" "update_assignment_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/update_assignment.py"
  output_path = "${path.module}/../../../lambda/update_assignment.zip"
}

resource "aws_lambda_function" "update_assignment" {
  filename         = data.archive_file.update_assignment_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-update-assignment"
  role            = var.lambda_role_arn
  handler         = "update_assignment.lambda_handler"
  source_code_hash = data.archive_file.update_assignment_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      ASSIGNMENTS_TABLE_NAME = var.assignments_table_name
      S3_BUCKET_NAME        = var.s3_bucket_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-update-assignment"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "update_assignment_logs" {
  name              = "/aws/lambda/${aws_lambda_function.update_assignment.function_name}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "update_assignment_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.update_assignment.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}

# Lambda: Delete Assignment
data "archive_file" "delete_assignment_zip" {
  type        = "zip"
  source_file = "${path.module}/../../../lambda/delete_assignment.py"
  output_path = "${path.module}/../../../lambda/delete_assignment.zip"
}

resource "aws_lambda_function" "delete_assignment" {
  filename         = data.archive_file.delete_assignment_zip.output_path
  function_name    = "${var.project_name}-${var.environment}-delete-assignment"
  role            = var.lambda_role_arn
  handler         = "delete_assignment.lambda_handler"
  source_code_hash = data.archive_file.delete_assignment_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = 30

  environment {
    variables = {
      ASSIGNMENTS_TABLE_NAME = var.assignments_table_name
      S3_BUCKET_NAME        = var.s3_bucket_name
    }
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-delete-assignment"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "delete_assignment_logs" {
  name              = "/aws/lambda/${aws_lambda_function.delete_assignment.function_name}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_lambda_permission" "delete_assignment_permission" {
  statement_id  = "AllowAPIGatewayInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.delete_assignment.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${var.api_execution_arn}/*/*"
}
