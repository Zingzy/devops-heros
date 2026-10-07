# IAM: governance

## What is IAM?

IAM (Identity and Access Management) decides who can call which AWS API on
which resource. Every request, from the console, the CLI or Terraform, is signed
by some identity, and IAM checks that identity's policies before it runs. IAM is
global, not tied to a region, and free.

## Users

A long lived identity in one account, with a console password, access keys, or
both. AWS now recommends IAM Identity Center for people (central sign-in, short
lived credentials) and keeping IAM users for the rare tool that cannot assume a
role. The root user, the email that opened the account, can do everything. It
should have MFA, no access keys, and almost never be used.

## Groups

A set of users. Policies attached to the group apply to every member, so access
is managed in one place. Groups cannot contain groups, and a group cannot be
named as a principal in a resource policy.

## Roles

An identity with permissions but no password or long term keys. Whoever assumes
it gets temporary credentials from STS (one hour by default). A role has a trust
policy (who may assume it, for example `ec2.amazonaws.com` or a GitHub Actions
OIDC provider) and permission policies (what it can do). EC2 instances, Lambda
functions, CI pipelines and Identity Center users should all get access through
roles.

## Policies

JSON documents of statements, each with `Effect`, `Action`, `Resource` and an
optional `Condition`.

- AWS managed: written by AWS, broad, such as `ReadOnlyAccess`.
- Customer managed: my own, reusable, versioned, with an ARN.
- Inline: lives inside one user, group or role and is deleted with it.
- Resource based: attached to a resource, such as a bucket policy. Has a
  `Principal`.
- Permissions boundaries, SCPs and RCPs: upper limits that never grant anything.

## Permissions

Everything starts as an implicit deny. A matching explicit `Deny` anywhere wins
over everything. Otherwise a matching `Allow` grants access, as long as every
boundary and SCP that applies also allows it.

## Least privilege

Give each identity only the actions and resources it needs: `s3:GetObject` on
one bucket, not `s3:*` on `*`. Start from what the workload actually calls (IAM
Access Analyzer can generate a policy from CloudTrail history) and narrow
further with conditions such as `aws:SourceIp` or `aws:SecureTransport`.

## IAM best practices

- MFA on the root user and every human. No root access keys.
- Identity Center and roles for people, roles for workloads. Avoid long lived
  access keys, and rotate any that must exist.
- Attach policies to groups or roles, not individual users. Prefer customer
  managed over inline policies.
- Use permissions boundaries and SCPs as guardrails, and review unused access
  with Access Analyzer. Keep CloudTrail on.

## Common use cases

An EC2 instance reading S3 through an instance profile with no keys on the box,
GitHub Actions deploying through OIDC into a role, cross account access from a
tooling account, and read only access for auditors.

## Example: a least privilege role

Run on my account with the AWS CLI. The account ID is shown as `<account-id>`.
The managed policy (`s3-read-policy.json`) allows `s3:ListBucket` on
`arn:aws:s3:::devops-hw18-reports` and `s3:GetObject` on
`arn:aws:s3:::devops-hw18-reports/*`. The trust policy (`ec2-trust.json`) lets
only `ec2.amazonaws.com` assume the role. An inline policy allows writing to one
log group.

```bash
aws iam create-policy --region ap-south-1 --policy-name devops-hw18-reports-read \
  --policy-document file://s3-read-policy.json \
  --tags Key=Project,Value=devops-homework Key=Session,Value=18 Key=Owner,Value=24bcs10177 \
  --query 'Policy.[PolicyName,Arn,DefaultVersionId]' --output text
aws iam create-role --region ap-south-1 --role-name devops-hw18-app-server-role \
  --assume-role-policy-document file://ec2-trust.json \
  --tags Key=Project,Value=devops-homework Key=Session,Value=18 Key=Owner,Value=24bcs10177 \
  --query 'Role.[RoleName,Arn]' --output text
aws iam attach-role-policy --region ap-south-1 --role-name devops-hw18-app-server-role \
  --policy-arn arn:aws:iam::<account-id>:policy/devops-hw18-reports-read
aws iam put-role-policy --region ap-south-1 --role-name devops-hw18-app-server-role \
  --policy-name devops-hw18-write-app-logs --policy-document file://inline-logs.json
```

```
devops-hw18-reports-read	arn:aws:iam::<account-id>:policy/devops-hw18-reports-read	v1
devops-hw18-app-server-role	arn:aws:iam::<account-id>:role/devops-hw18-app-server-role
```

The policy simulator checks what the role may do without making the calls:

```bash
aws iam simulate-principal-policy --region ap-south-1 \
  --policy-source-arn arn:aws:iam::<account-id>:role/devops-hw18-app-server-role \
  --action-names s3:GetObject s3:PutObject s3:DeleteObject logs:PutLogEvents \
  --resource-arns arn:aws:s3:::devops-hw18-reports/q3.csv \
  --query 'EvaluationResults[].[EvalActionName,EvalDecision]' --output text
```

```
s3:GetObject	allowed
s3:PutObject	implicitDeny
s3:DeleteObject	implicitDeny
logs:PutLogEvents	implicitDeny
```

Read only, as intended. `implicitDeny` means nothing allowed it, not that a
policy denied it. (`logs:PutLogEvents` is denied here only because I asked about
an S3 object.)

The trust policy is enforced too. My own user cannot assume the role:

```bash
aws sts assume-role --region ap-south-1 \
  --role-arn arn:aws:iam::<account-id>:role/devops-hw18-app-server-role \
  --role-session-name test --query 'Credentials.Expiration' --output text
```

```

aws: [ERROR]: An error occurred (AccessDenied) when calling the AssumeRole operation: User: arn:aws:iam::<account-id>:user/<iam-user> is not authorized to perform: sts:AssumeRole on resource: arn:aws:iam::<account-id>:role/devops-hw18-app-server-role
```

Clean-up. IAM refuses to delete a role that still has policies (`DeleteConflict`),
so the inline policy goes first and the managed one is detached:

```bash
aws iam delete-role-policy --region ap-south-1 --role-name devops-hw18-app-server-role \
  --policy-name devops-hw18-write-app-logs
aws iam detach-role-policy --region ap-south-1 --role-name devops-hw18-app-server-role \
  --policy-arn arn:aws:iam::<account-id>:policy/devops-hw18-reports-read
aws iam delete-role --region ap-south-1 --role-name devops-hw18-app-server-role
aws iam delete-policy --region ap-south-1 \
  --policy-arn arn:aws:iam::<account-id>:policy/devops-hw18-reports-read
```

All four printed nothing, which means success.
