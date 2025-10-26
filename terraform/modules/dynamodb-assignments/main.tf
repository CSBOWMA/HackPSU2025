resource "aws_dynamodb_table" "assignments_table" {
  name           = "${var.project_name}-${var.environment}-assignments"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_id"
  range_key      = "assignment_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "assignment_id"
    type = "S"
  }

  attribute {
    name = "class_id"
    type = "S"
  }

  attribute {
    name = "due_date"
    type = "S"
  }

  # GSI for querying by class
  global_secondary_index {
    name            = "user_id-class_id-index"
    hash_key        = "user_id"
    range_key       = "class_id"
    projection_type = "ALL"
  }

  # GSI for querying by due date
  global_secondary_index {
    name            = "user_id-due_date-index"
    hash_key        = "user_id"
    range_key       = "due_date"
    projection_type = "ALL"
  }

  tags = {
    Name        = "${var.project_name}-${var.environment}-assignments"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
