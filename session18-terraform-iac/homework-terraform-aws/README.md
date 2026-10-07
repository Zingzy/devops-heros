# Session 18: Terraform and Infrastructure as Code

- Name: Aditya Singhi
- Enrollment number: 24BCS10177

Run on my own AWS account in `ap-south-1` with Terraform v1.16.4, the
hashicorp/aws provider v6.67.0 and the AWS CLI v2. Every resource was named
`devops-hw18-`, tagged `Project=devops-homework`, `Session=18`,
`Owner=24bcs10177`, and deleted in the same session. The account ID is masked as
`<account-id>` and my IAM user name as `<iam-user>`.

## Task 1: Terraform S3 demo

[terraform-s3-demo/](terraform-s3-demo/README.md) has the six files the
assignment lists and the full walkthrough of `init`, `fmt`, `validate`, `plan`,
`apply`, `show`, `output` and `destroy`, with real output for each.

```text
terraform-s3-demo/
|-- main.tf            aws_s3_bucket + aws_s3_bucket_versioning
|-- variables.tf       region, bucket name (with a validation rule), environment
|-- outputs.tf         bucket name, ARN, region, versioning status
|-- provider.tf        terraform block and the aws provider with default_tags
|-- terraform.tfvars   the values used
`-- README.md
```

```bash
terraform plan -out=demo.tfplan
echo yes | terraform apply
terraform plan -detailed-exitcode
echo yes | terraform destroy
```

```
...
Plan: 2 to add, 0 to change, 0 to destroy.
...
Apply complete! Resources: 2 added, 0 changed, 0 destroyed.
...
No changes. Your infrastructure matches the configuration.
...
Destroy complete! Resources: 2 destroyed.
```

The bucket `devops-hw18-24bcs10177-68535f` was created with versioning and all
six tags, a second `plan` found no drift, and `destroy` removed it even with
object versions inside, thanks to `force_destroy`.

![terraform apply](screenshots/01-terraform-apply.png)

![terraform destroy](screenshots/02-terraform-destroy.png)

## Task 2: AWS services research

One README per service, covering every point the assignment lists, each with
one example run on the same account:

| Service | Example |
|---|---|
| [01-iam](aws-services/01-iam/README.md) | A `devops-hw18-` role with managed and inline policies, checked with the policy simulator |
| [02-ec2](aws-services/02-ec2/README.md) | A t3.micro launched, stopped, started with and without an Elastic IP, terminated |
| [03-s3](aws-services/03-s3/README.md) | New bucket defaults, versioning and delete markers, a deny-HTTP bucket policy |
| [04-vpc](aws-services/04-vpc/README.md) | A 12 resource Terraform VPC ([main.tf](aws-services/04-vpc/main.tf)) with public and private subnets and a NAT Gateway |
| [05-dynamodb-rds](aws-services/05-dynamodb-rds/README.md) | An on-demand DynamoDB table queried by partition and sort key. RDS engine and instance options, no instance created |


## Clean-up check

After everything was deleted, direct checks by tag and by name prefix in
`ap-south-1`:

```bash
aws ec2 describe-instances --region ap-south-1 --filters Name=tag:Session,Values=18 \
  --query 'Reservations[].Instances[].[InstanceId,State.Name]' --output text
aws ec2 describe-vpcs --region ap-south-1 --filters Name=tag:Session,Values=18 --query 'Vpcs[].VpcId' --output text
aws ec2 describe-nat-gateways --region ap-south-1 --filter Name=tag:Session,Values=18 \
  --query 'NatGateways[].[NatGatewayId,State]' --output text
aws ec2 describe-addresses --region ap-south-1 --filters Name=tag:Session,Values=18 \
  --query 'Addresses[].[AllocationId,PublicIp]' --output text
aws ec2 describe-volumes --region ap-south-1 --filters Name=tag:Session,Values=18 --query 'Volumes[].VolumeId' --output text
aws s3api list-buckets --region ap-south-1 --query "Buckets[?starts_with(Name,'devops-hw18-')].Name" --output text
aws iam list-roles --region ap-south-1 --query "Roles[?starts_with(RoleName,'devops-hw18-')].RoleName" --output text
aws dynamodb list-tables --region ap-south-1 --query "TableNames[?starts_with(@,'devops-hw18-')]" --output text
```

```
i-012b58f74ec4d2a4c	terminated
nat-0f7eb6c34d01c769d	deleted
```

Only the terminated instance and the deleted NAT Gateway still show, and AWS
keeps both visible for about an hour without billing them. No VPC, Elastic IP,
volume, bucket, role or table is left.

## Notes

- The instructor's `outputs.tf` uses `type` on output blocks, which only exists
  since Terraform 1.15, but declares `required_version = ">= 1.6.0"`. Mine
  requires `>= 1.15.0`.
- The session `.gitignore` ignores `terraform.tfvars`, which the assignment asks
  for. This folder's `.gitignore` adds an exception for it, and also ignores a
  plan file named plain `tfplan`, which `*.tfplan` misses.
- The NAT Gateway took 2m5s of the VPC's 142 second apply. Every other resource
  took a second or two.
- New S3 buckets come with SSE-S3 encryption and Block Public Access on, but EBS
  encryption by default was off in this account, so the EC2 root volume was
  unencrypted.
- Terminating an instance does not release its Elastic IP. It keeps billing
  until `release-address`.
