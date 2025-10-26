resource "aws_s3_bucket" "rag_data" {
  bucket = "${var.project_name}-${var.environment}-rag-data"

  tags = {
    Name        = "${var.project_name}-${var.environment}-rag-data"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Purpose     = "RAG-Model-Data"
  }
}

# Block all public access (SECURITY BEST PRACTICE)
resource "aws_s3_bucket_public_access_block" "rag_data" {
  bucket = aws_s3_bucket.rag_data.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# Enable versioning (helpful for data management)
resource "aws_s3_bucket_versioning" "rag_data" {
  bucket = aws_s3_bucket.rag_data.id

  versioning_configuration {
    status = "Enabled"
  }
}

# Server-side encryption
resource "aws_s3_bucket_server_side_encryption_configuration" "rag_data" {
  bucket = aws_s3_bucket.rag_data.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Lifecycle rule to manage costs (optional)
resource "aws_s3_bucket_lifecycle_configuration" "rag_data" {
  bucket = aws_s3_bucket.rag_data.id

  rule {
    id     = "transition-to-ia"
    status = "Enabled"

    filter {
      prefix = ""  # Apply to all objects
    }

    transition {
      days          = 90
      storage_class = "STANDARD_IA"
    }
  }

  rule {
    id     = "delete-old-versions"
    status = "Enabled"

    filter {
      prefix = ""  # Apply to all objects
    }

    noncurrent_version_expiration {
      noncurrent_days = 30
    }
  }
}

# CORS configuration (if you need browser uploads)
resource "aws_s3_bucket_cors_configuration" "rag_data" {
  bucket = aws_s3_bucket.rag_data.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE", "HEAD"]
    allowed_origins = ["*"]  # Restrict this to your domain in production
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

# IAM policy for Lambda to access the bucket
resource "aws_iam_role_policy" "lambda_s3_policy" {
  name = "${var.project_name}-${var.environment}-lambda-s3-policy"
  role = var.lambda_role_name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.rag_data.arn,
          "${aws_s3_bucket.rag_data.arn}/*"
        ]
      }
    ]
  })
}

# ==================== IAM USER FOR S3 ACCESS ====================

# Create IAM User for S3 bucket access
resource "aws_iam_user" "s3_user" {
  name = "${var.project_name}-${var.environment}-s3-user"

  tags = {
    Name        = "${var.project_name}-${var.environment}-s3-user"
    Environment = var.environment
    ManagedBy   = "Terraform"
    Purpose     = "S3-RAG-Bucket-Access"
  }
}

# Create access key for the user
resource "aws_iam_access_key" "s3_user_key" {
  user = aws_iam_user.s3_user.name
}

# Create inline policy for full S3 bucket access
resource "aws_iam_user_policy" "s3_user_policy" {
  name = "${var.project_name}-${var.environment}-s3-user-policy"
  user = aws_iam_user.s3_user.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:*"
        ]
        Resource = [
          aws_s3_bucket.rag_data.arn,
          "${aws_s3_bucket.rag_data.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = aws_s3_bucket.rag_data.arn
      }
    ]
  })
}
