# VPC: networking

## What is VPC?

A VPC (Virtual Private Cloud) is my own private network in one AWS region. I
choose its IP range, split it into subnets, and decide what can reach the
internet. EC2, RDS, load balancers and Lambda functions in a VPC get their IPs
from it. Every region has a default VPC (`172.31.0.0/16`) for quick experiments.

## CIDR

CIDR notation is an address plus a prefix length: `10.0.0.0/16` fixes the first
16 bits and leaves 65,536 addresses, `/24` leaves 256. A VPC block can be `/16`
down to `/28`. Use the private RFC 1918 ranges and avoid overlapping other VPCs
or the office network, because overlapping networks cannot be peered later.

## Subnets

A slice of the VPC range in exactly one Availability Zone. AWS reserves 5
addresses in each (network, router, DNS, one spare, broadcast), so a `/24` has
251 usable. The usual layout is a public and a private subnet in each of two or
more AZs.

## Route tables

Rules of destination CIDR to target that decide where traffic from a subnet
goes. The most specific match wins. Every route table has a `local` route for the
VPC's own range, which is why subnets can always reach each other. Each subnet
uses one route table, the main one if none is associated.

## Internet Gateway

Connects the VPC to the internet. One per VPC, managed and scaled by AWS. An
instance is reachable from the internet only if its subnet routes `0.0.0.0/0` to
the IGW and it has a public IP.

## NAT Gateway

Lets instances in private subnets start outbound connections (updates, API
calls) while nothing can connect in. A zonal NAT Gateway sits in a public subnet
with an Elastic IP, so high availability needs one per AZ. Since November 2025 a
regional NAT Gateway can span AZs by itself. It bills per hour and per GB, so
S3 and DynamoDB traffic should use free gateway endpoints instead.

## Security Groups

Stateful firewalls on each network interface. Allow rules only, all evaluated
together, and they can reference other security groups.

## Network ACLs

Stateless firewalls at the subnet edge. Rules are numbered and evaluated from
lowest to highest, first match wins, and they can deny as well as allow. Return
traffic needs its own rule (ephemeral ports 1024 to 65535). Every NACL ends with
a `*` deny rule. The default NACL allows everything, a new custom one denies
everything until rules are added.

## Public vs private subnet

A subnet is public only because its route table sends `0.0.0.0/0` to an IGW.
Load balancers and NAT Gateways go there. A private subnet has no route to the
IGW, and reaches out through a NAT Gateway if at all. App servers and databases
go there.

## Example: a two tier VPC in Terraform

[main.tf](main.tf) builds a VPC, a public and a private subnet, an IGW, a NAT
Gateway with its Elastic IP, two route tables and their associations, a security
group and a NACL: 12 resources, all named `devops-hw18-` and tagged through
`default_tags`. The public route table sends `0.0.0.0/0` to the IGW, the
private one sends it to the NAT Gateway, and the NAT Gateway has
`depends_on = [aws_internet_gateway.igw]` because AWS wants the IGW attached
first.

I applied it on my account in `ap-south-1`:

```bash
terraform init
terraform apply -auto-approve
```

```
aws_eip.nat: Creating...
aws_vpc.main: Creating...
...
aws_subnet.public: Creation complete after 11s [id=subnet-0c6085e9f7af04cbc]
...
aws_nat_gateway.nat: Still creating... [02m01s elapsed]
aws_nat_gateway.nat: Creation complete after 2m5s [id=nat-0f7eb6c34d01c769d]
aws_route_table.private: Creating...
...
Apply complete! Resources: 12 added, 0 changed, 0 destroyed.

Outputs:

nat_public_ip = "3.108.179.17"
private_route_table = [
  "0.0.0.0/0 -> nat-0f7eb6c34d01c769d",
]
public_route_table = [
  "0.0.0.0/0 -> igw-03ecd69127b934373",
]
...
```

The NAT Gateway took 2 minutes 5 seconds of a 142 second apply. Every other
resource took a second or two. The private route table waited for it, because it
references the NAT Gateway's ID.

Checking the result with the CLI:

```bash
aws ec2 describe-route-tables --region ap-south-1 --filters Name=vpc-id,Values=vpc-01cc91dae5ea89125 \
  --query 'RouteTables[].[Tags[?Key==`Name`]|[0].Value,Routes[].[DestinationCidrBlock,GatewayId||NatGatewayId,State]]' --output text
aws ec2 describe-subnets --region ap-south-1 --filters Name=vpc-id,Values=vpc-01cc91dae5ea89125 \
  --query 'Subnets[].[Tags[?Key==`Name`]|[0].Value,CidrBlock,AvailableIpAddressCount,MapPublicIpOnLaunch]' --output text
aws ec2 describe-network-acls --region ap-south-1 \
  --filters Name=vpc-id,Values=vpc-01cc91dae5ea89125 Name=default,Values=false \
  --query 'NetworkAcls[0].Entries[].[Egress,RuleNumber,Protocol,RuleAction,CidrBlock,PortRange.From,PortRange.To]' --output text
```

```
None
10.0.0.0/16	local	active
devops-hw18-public-rt
10.0.0.0/16	local	active
0.0.0.0/0	igw-03ecd69127b934373	active
devops-hw18-private-rt
10.0.0.0/16	local	active
0.0.0.0/0	nat-0f7eb6c34d01c769d	active
devops-hw18-public-1a	10.0.1.0/24	250	True
devops-hw18-private-1a	10.0.11.0/24	251	False
True	100	-1	allow	0.0.0.0/0	None	None
True	32767	-1	deny	0.0.0.0/0	None	None
False	100	6	allow	0.0.0.0/0	443	443
False	110	6	allow	0.0.0.0/0	1024	65535
False	32767	-1	deny	0.0.0.0/0	None	None
```

- The unnamed route table is the main one AWS created with the VPC. All three
  have the `local` route without my writing it. The public one routes to the
  IGW and the private one to the NAT Gateway, which is the whole difference
  between the two subnets.
- The private subnet shows 251 free addresses, 256 minus the 5 reserved. The
  public one shows 250 because the NAT Gateway's interface took one.
- In the NACL, `True` rows are outbound. Rule 110 allows the ephemeral return
  ports, and rule 32767 is the final `*` deny that I never wrote and cannot
  remove.

I used the public subnet for the [EC2 example](../02-ec2/README.md), then
destroyed everything:

```bash
terraform destroy -auto-approve
```

```
...
aws_nat_gateway.nat: Destruction complete after 1m1s
...
aws_vpc.main: Destruction complete after 1s

Destroy complete! Resources: 12 destroyed.
```

The VPC was up for about 11 minutes, and the NAT Gateway was again the slow part
of the destroy.
