terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

# The emulator accepts any credentials, the provider only needs something non-empty.
provider "aws" {
  region     = var.aws_region
  access_key = "test"
  secret_key = "test"

  skip_credentials_validation = true
  skip_metadata_api_check     = true
  skip_requesting_account_id  = true

  # Without path style the provider asks for <bucket>.localhost, which does not resolve.
  s3_use_path_style = true

  endpoints {
    ec2 = var.aws_endpoint
    s3  = var.aws_endpoint
    sts = var.aws_endpoint
  }

  default_tags {
    tags = {
      Project   = var.project
      Session   = "19"
      ManagedBy = "Terraform"
    }
  }
}
