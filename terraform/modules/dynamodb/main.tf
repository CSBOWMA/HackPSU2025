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
    ManagedBy   = "Terraform"
  }
}
