resource "aws_dynamodb_table" "classes_table" {
  name           = "${var.project_name}-${var.environment}-classes"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  range_key      = "class_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "class_id"
    type = "S"
  }

  attribute {
    name = "semester"
    type = "S"
  }

  # GSI for querying by semester
  global_secondary_index {
    name            = "user_id-semester-index"
    hash_key        = "user_id"
    range_key       = "semester"
    projection_type = "ALL"
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-classes"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
