output "vpc_id" {
  description = "ID of the VPC."
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "ID of the public subnet."
  value       = aws_subnet.public.id
}

output "security_group_id" {
  description = "ID of the web security group."
  value       = aws_security_group.web.id
}

output "instance_id" {
  description = "ID of the EC2 web server."
  value       = aws_instance.web.id
}

output "instance_private_ip" {
  description = "Private IP the instance got from the subnet."
  value       = aws_instance.web.private_ip
}

output "instance_public_ip" {
  description = "Public IP, assigned because the subnet maps public IPs on launch."
  value       = aws_instance.web.public_ip
}

output "bucket_name" {
  description = "Name of the S3 bucket."
  value       = aws_s3_bucket.artifacts.bucket
}

output "web_url" {
  description = "Where nginx answers once the instance has booted."
  value       = "http://${aws_instance.web.public_ip}"
}

output "ami_name" {
  description = "Image the data source picked."
  value       = data.aws_ami.al2023.name
}
