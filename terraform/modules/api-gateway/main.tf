# API Gateway
resource "aws_apigatewayv2_api" "chat_api" {
  name          = "${var.project_name}-${var.environment}-api"
  protocol_type = "HTTP"
  
  cors_configuration {
    allow_origins     = ["*"]  # Change to specific domain in production
    allow_methods     = ["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"]
    allow_headers     = ["*"]
    expose_headers    = ["*"]
    max_age           = 300
    allow_credentials = false
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-api"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_cloudwatch_log_group" "api_gateway_logs" {
  name              = "/aws/apigateway/${var.project_name}-${var.environment}"
  retention_in_days = 7

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
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

  tags = {
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

# ==================== CHAT INTEGRATIONS ====================

resource "aws_apigatewayv2_integration" "create_chat_integration" {
  api_id           = aws_apigatewayv2_api.chat_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = var.create_chat_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "get_chat_integration" {
  api_id           = aws_apigatewayv2_api.chat_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = var.get_chat_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "list_chats_integration" {
  api_id           = aws_apigatewayv2_api.chat_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = var.list_chats_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "delete_chat_integration" {
  api_id           = aws_apigatewayv2_api.chat_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = var.delete_chat_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "append_message_integration" {
  api_id           = aws_apigatewayv2_api.chat_api.id
  integration_type = "AWS_PROXY"
  integration_uri  = var.append_message_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

# ==================== CLASSES INTEGRATIONS ====================

resource "aws_apigatewayv2_integration" "get_all_classes_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.get_all_classes_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "get_class_by_id_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.get_class_by_id_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "create_class_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.create_class_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "update_class_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.update_class_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "delete_class_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.delete_class_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

# ==================== CHAT ROUTES ====================

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

# ==================== CLASSES ROUTES ====================

resource "aws_apigatewayv2_route" "get_all_classes_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "GET /users/{user_id}/classes"
  target    = "integrations/${aws_apigatewayv2_integration.get_all_classes_integration.id}"
}

resource "aws_apigatewayv2_route" "get_class_by_id_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "GET /users/{user_id}/classes/{class_id}"
  target    = "integrations/${aws_apigatewayv2_integration.get_class_by_id_integration.id}"
}

resource "aws_apigatewayv2_route" "create_class_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "POST /users/{user_id}/classes"
  target    = "integrations/${aws_apigatewayv2_integration.create_class_integration.id}"
}

resource "aws_apigatewayv2_route" "update_class_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "PUT /users/{user_id}/classes/{class_id}"
  target    = "integrations/${aws_apigatewayv2_integration.update_class_integration.id}"
}

resource "aws_apigatewayv2_route" "delete_class_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "DELETE /users/{user_id}/classes/{class_id}"
  target    = "integrations/${aws_apigatewayv2_integration.delete_class_integration.id}"
}

# ==================== ASSIGNMENTS INTEGRATIONS ====================

resource "aws_apigatewayv2_integration" "list_assignments_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.list_assignments_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "get_assignment_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.get_assignment_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "create_assignment_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.create_assignment_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "update_assignment_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.update_assignment_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_integration" "delete_assignment_integration" {
  api_id             = aws_apigatewayv2_api.chat_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = var.delete_assignment_invoke_arn
  integration_method = "POST"
  payload_format_version = "2.0"
}

# ==================== ASSIGNMENTS ROUTES ====================

resource "aws_apigatewayv2_route" "list_assignments_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "GET /users/{user_id}/assignments"
  target    = "integrations/${aws_apigatewayv2_integration.list_assignments_integration.id}"
}

resource "aws_apigatewayv2_route" "get_assignment_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "GET /users/{user_id}/assignments/{assignment_id}"
  target    = "integrations/${aws_apigatewayv2_integration.get_assignment_integration.id}"
}

resource "aws_apigatewayv2_route" "create_assignment_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "POST /users/{user_id}/assignments"
  target    = "integrations/${aws_apigatewayv2_integration.create_assignment_integration.id}"
}

resource "aws_apigatewayv2_route" "update_assignment_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "PUT /users/{user_id}/assignments/{assignment_id}"
  target    = "integrations/${aws_apigatewayv2_integration.update_assignment_integration.id}"
}

resource "aws_apigatewayv2_route" "delete_assignment_route" {
  api_id    = aws_apigatewayv2_api.chat_api.id
  route_key = "DELETE /users/{user_id}/assignments/{assignment_id}"
  target    = "integrations/${aws_apigatewayv2_integration.delete_assignment_integration.id}"
}
