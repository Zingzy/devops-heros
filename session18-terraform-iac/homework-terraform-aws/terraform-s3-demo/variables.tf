variable "aws_region" {
  type        = string
  description = "AWS region for the bucket."
  default     = "ap-south-1"
}

variable "bucket_name" {
  type        = string
  description = "Name of the S3 bucket. Must be lowercase, 3 to 63 characters."

  validation {
    condition     = can(regex("^[a-z0-9][a-z0-9.-]{1,61}[a-z0-9]$", var.bucket_name))
    error_message = "Bucket names must be 3 to 63 characters of lowercase letters, numbers, dots and hyphens."
  }
}

variable "environment" {
  type        = string
  description = "Environment tag."
  default     = "dev"
}
