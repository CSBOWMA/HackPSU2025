output "bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.rag_data.id
}

output "bucket_arn" {
  description = "S3 bucket ARN"
  value       = aws_s3_bucket.rag_data.arn
}

output "bucket_domain_name" {
  description = "S3 bucket domain name"
  value       = aws_s3_bucket.rag_data.bucket_domain_name
}

output "bucket_regional_domain_name" {
  description = "S3 bucket regional domain name"
  value       = aws_s3_bucket.rag_data.bucket_regional_domain_name
}

# IAM User Outputs
output "iam_user_name" {
  description = "IAM user name for S3 access"
  value       = aws_iam_user.s3_user.name
}

output "iam_user_arn" {
  description = "IAM user ARN"
  value       = aws_iam_user.s3_user.arn
}

output "access_key_id" {
  description = "AWS Access Key ID for S3 user"
  value       = aws_iam_access_key.s3_user_key.id
}

output "secret_access_key" {
  description = "AWS Secret Access Key for S3 user"
  value       = aws_iam_access_key.s3_user_key.secret
  sensitive   = true
}
