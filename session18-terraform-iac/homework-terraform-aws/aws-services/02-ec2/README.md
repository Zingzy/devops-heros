# EC2: compute

## What is EC2?

EC2 (Elastic Compute Cloud) rents virtual machines, called instances, billed per
second while running. On-Demand has no commitment, Savings Plans trade a one or
three year commitment for a discount, and Spot is cheap spare capacity that AWS
can take back with two minutes' warning.

## AMI

An AMI (Amazon Machine Image) is the template an instance boots from: root
volume snapshot, architecture and boot settings. AMIs are regional, built for one
architecture, and their IDs change with every patch release, so look them up
through the public SSM parameters instead of hardcoding them.

## Instance types

The name encodes the hardware. `m7g.large` is family `m` (general purpose),
generation 7, `g` for Graviton (ARM), size `large`. Families: general purpose
(`t`, `m`), compute optimized (`c`), memory optimized (`r`, `x`), storage
optimized (`i`, `d`), and accelerated with GPUs or ML chips (`g`, `p`, `inf`,
`trn`). `t` types are burstable: they earn CPU credits while idle and spend them
on spikes, which suits small web apps but not steady CPU load.

## Key pairs

AWS stores the public key and puts it on the instance at first boot. The private
key is shown once at creation and AWS does not keep it. Types are RSA and
ED25519 (ED25519 does not work for Windows). Session Manager and EC2 Instance
Connect let you log in without keeping SSH keys or opening port 22.

## Security Groups

A firewall on the instance's network interface. Rules only allow, never deny.
With no inbound rules nothing gets in, and by default all outbound is allowed.
It is stateful, so reply traffic is allowed automatically. A rule can name
another security group as the source, which works better than IP ranges.

## EBS

EBS volumes are network disks in one Availability Zone. `gp3` is the default
SSD, with 3,000 IOPS and 125 MiB/s at any size. `io2` is for heavy databases.
Snapshots are incremental backups stored in S3. The root volume has
`DeleteOnTermination` on by default, extra volumes do not.

## Public vs private IP

The private IP comes from the subnet and stays for the instance's whole life. An
auto assigned public IP is released on stop and a new one is given on start. An
Elastic IP is a static public address that stays until you release it. Since
February 2024 every public IPv4 address is billed, about $0.005 an hour.

## Instance lifecycle

`pending` -> `running` -> `stopping` -> `stopped` -> `pending` again on start,
and `shutting-down` -> `terminated` from either running or stopped. Running is
billed for compute. Stopped is not, but its EBS volumes and Elastic IPs are.
Terminated is permanent.

## Common use cases

Web servers in an Auto Scaling group, software that needs OS access, CI runners
on Spot, and GPU workloads.

## Example: launching and cycling a t3.micro

Run on my account in `ap-south-1`, in the public subnet of the VPC from the
[VPC notes](../04-vpc/README.md). The instance ran for a few minutes. The
instance profile wraps the role from the [IAM notes](../01-iam/README.md). The
key pair `devops-hw18-ed25519` and security group `devops-hw18-ssh-http` were
created just before.

```bash
aws ssm get-parameter --region ap-south-1 \
  --name /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64 \
  --query 'Parameter.[Value,LastModifiedDate]' --output text
aws ec2 run-instances --region ap-south-1 --image-id ami-08e3b3155fc937a94 --instance-type t3.micro \
  --key-name devops-hw18-ed25519 --subnet-id subnet-0c6085e9f7af04cbc \
  --security-group-ids sg-05ea3162075bd00b6 \
  --iam-instance-profile Name=devops-hw18-app-server-profile \
  --metadata-options HttpTokens=required \
  --block-device-mappings 'DeviceName=/dev/xvda,Ebs={VolumeSize=20,VolumeType=gp3,DeleteOnTermination=true}' \
  --tag-specifications \
    'ResourceType=instance,Tags=[{Key=Name,Value=devops-hw18-web},{Key=Project,Value=devops-homework},{Key=Session,Value=18},{Key=Owner,Value=24bcs10177}]' \
    'ResourceType=volume,Tags=[{Key=Name,Value=devops-hw18-web-root},{Key=Project,Value=devops-homework},{Key=Session,Value=18},{Key=Owner,Value=24bcs10177}]' \
  --query 'Instances[0].[InstanceId,State.Name]' --output text
aws ec2 describe-volumes --region ap-south-1 --filters Name=attachment.instance-id,Values=i-012b58f74ec4d2a4c \
  --query 'Volumes[].[VolumeId,VolumeType,Size,Iops,Throughput,AvailabilityZone,Attachments[0].DeleteOnTermination,Encrypted]' \
  --output text
```

```
ami-08e3b3155fc937a94	2026-10-01T04:53:15.004000+05:30
i-012b58f74ec4d2a4c	pending
vol-0e4ae046344a93ad8	gp3	20	3000	125	ap-south-1a	True	False
```

The volume got the gp3 baseline without asking. `Encrypted False` shows that EBS
encryption by default is off in this account and region, which I would turn on
for real work. `HttpTokens=required` forces IMDSv2 on the metadata service.

Stop and start, and watch the IPs:

```bash
aws ec2 describe-instances --region ap-south-1 --instance-ids i-012b58f74ec4d2a4c \
  --query 'Reservations[0].Instances[0].[State.Name,InstanceType,Placement.AvailabilityZone,PrivateIpAddress,PublicIpAddress,MetadataOptions.HttpTokens]' \
  --output text
aws ec2 stop-instances --region ap-south-1 --instance-ids i-012b58f74ec4d2a4c \
  --query 'StoppingInstances[0].[PreviousState.Name,CurrentState.Name]' --output text
aws ec2 wait instance-stopped --region ap-south-1 --instance-ids i-012b58f74ec4d2a4c
aws ec2 describe-instances --region ap-south-1 --instance-ids i-012b58f74ec4d2a4c \
  --query 'Reservations[0].Instances[0].[State.Name,PrivateIpAddress,PublicIpAddress]' --output text
aws ec2 start-instances --region ap-south-1 --instance-ids i-012b58f74ec4d2a4c \
  --query 'StartingInstances[0].[PreviousState.Name,CurrentState.Name]' --output text
aws ec2 wait instance-running --region ap-south-1 --instance-ids i-012b58f74ec4d2a4c
aws ec2 describe-instances --region ap-south-1 --instance-ids i-012b58f74ec4d2a4c \
  --query 'Reservations[0].Instances[0].[State.Name,PrivateIpAddress,PublicIpAddress]' --output text
```

```
running	t3.micro	ap-south-1a	10.0.1.79	13.206.124.143	required
running	stopping
stopped	10.0.1.79	None
stopped	pending
running	10.0.1.79	13.207.176.57
```

The private IP stayed. The public IP was released on stop and came back
different. The stop took 15 seconds and the start 18. Then I allocated an
Elastic IP (`eipalloc-066fa1cd8134bf72e`, `15.207.48.214`), attached it with
`associate-address`, and stopped, described, started and described it again:

```
stopping
stopped	15.207.48.214
pending
running	10.0.1.79	15.207.48.214
```

The Elastic IP stayed through the stop and the start.

Terminate and clean up:

```bash
aws ec2 terminate-instances --region ap-south-1 --instance-ids i-012b58f74ec4d2a4c \
  --query 'TerminatingInstances[0].[PreviousState.Name,CurrentState.Name]' --output text
aws ec2 wait instance-terminated --region ap-south-1 --instance-ids i-012b58f74ec4d2a4c
aws ec2 describe-volumes --region ap-south-1 --filters Name=tag:Session,Values=18 --query 'length(Volumes)'
aws ec2 describe-addresses --region ap-south-1 --allocation-ids eipalloc-066fa1cd8134bf72e \
  --query 'Addresses[0].[PublicIp,InstanceId]' --output text
aws ec2 release-address --region ap-south-1 --allocation-id eipalloc-066fa1cd8134bf72e
aws ec2 delete-security-group --region ap-south-1 --group-id sg-05ea3162075bd00b6 --query Return --output text
aws ec2 delete-key-pair --region ap-south-1 --key-name devops-hw18-ed25519 --query Return --output text
```

```
running	shutting-down
0
15.207.48.214	None
True
True
```

The root volume went with the instance. The Elastic IP did not: termination
only detached it (`InstanceId` is `None`), and it keeps billing until released.
