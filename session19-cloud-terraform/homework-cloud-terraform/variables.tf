variable "aws_region" {
  description = "AWS region for every resource."
  type        = string
  default     = "ap-south-1"
}

variable "aws_endpoint" {
  description = "Where the AWS provider sends API calls. Points at the local AWS emulator."
  type        = string
  default     = "http://localhost:18190"
}

variable "project" {
  description = "Prefix used in resource names and tags."
  type        = string
  default     = "hw19"
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

variable "ssh_cidr" {
  description = "Only this range may reach port 22."
  type        = string
  default     = "203.0.113.10/32"
}
