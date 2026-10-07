terraform {
  # type on output blocks needs 1.15 or newer
  required_version = ">= 1.15.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project = "devops-homework"
      Session = "18"
      Owner   = "24bcs10177"
    }
  }
}
