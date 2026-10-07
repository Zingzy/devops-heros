variable "aws_region" {
  description = "AWS region for every resource."
  type        = string
  default     = "ap-south-1"

  validation {
    condition     = var.aws_region == "ap-south-1"
    error_message = "This lab may only run in ap-south-1."
  }
}

variable "project" {
  description = "Prefix used in every resource name."
  type        = string
  default     = "devops-hw19"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.19.0.0/16"
}

variable "public_subnet_cidr" {
  description = "CIDR block for the public subnet. Must sit inside vpc_cidr."
  type        = string
  default     = "10.19.1.0/24"
}

variable "instance_type" {
  description = "EC2 instance size."
  type        = string
  default     = "t3.micro"
}
