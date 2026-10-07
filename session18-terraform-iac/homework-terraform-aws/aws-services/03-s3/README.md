# S3: storage

## What is S3?

S3 (Simple Storage Service) stores files, called objects, in buckets and serves
them over HTTPS. There is no disk to size and no server to manage. You pay for
storage, requests and data going out. S3 Standard is designed for 11 nines of
durability by keeping copies in at least three Availability Zones, and reads have
been strongly consistent since 2020.

## Buckets

The top level container, created in one region. General purpose bucket names
are 3 to 63 lowercase characters, cannot be changed, and must be unique across
every AWS account, not just mine. An account can have 10,000 buckets by default.

## Objects

Data plus metadata, found by its key. `logs/2026/app.log` looks like a path,
but there are no real folders. Objects can be up to 50 TB (raised from 5 TB in
December 2025). One `PUT` takes up to 5 GB, and bigger files use multipart upload.

## Storage classes

Set per object. Colder is cheaper to store and costlier to read.

- Standard: frequent access, the default.
- Intelligent-Tiering: moves objects between tiers by itself.
- Standard-IA and One Zone-IA: read rarely but needed fast. 30 day minimum.
- Glacier Instant Retrieval: archives with millisecond reads. 90 day minimum.
- Glacier Flexible Retrieval and Deep Archive: restore before reading, minutes
  to hours. 90 and 180 day minimums.

## Versioning

A bucket is unversioned, versioning enabled, or suspended. It can never go back
to unversioned. With versioning on, an overwrite keeps the old copy, and a plain
delete only adds a delete marker on top, so removing the marker brings the
object back. Deleting a specific version ID is permanent. Every version is
billed.

## Lifecycle policies

Rules that move objects to colder classes after N days (transitions), delete
them after N days (expiration), expire old versions, and abort unfinished
multipart uploads. Objects under 128 KB are skipped by default for transitions.

## Encryption

Every new object is encrypted at rest, by default with SSE-S3 (keys managed by
AWS, free). SSE-KMS uses a KMS key, logged in CloudTrail, and Bucket Keys cut its
request cost. SSE-C (client supplied keys) is disabled by default on new buckets
since April 2026. In transit, every endpoint supports TLS, and a bucket policy
can require it.

## Bucket policies

A resource based policy on the bucket, with a `Principal`, up to 20 KB. It can
grant access to other accounts or services, or deny everyone under a condition.
New buckets also have Block Public Access on and ACLs disabled by default.

## Common use cases

Static website assets behind CloudFront, backups and archives with lifecycle
rules, data lakes queried by Athena, CI artifacts and logs, and Terraform remote
state.

## Example: defaults, versioning and a deny-HTTP policy

Run on my account in `ap-south-1`, on a throwaway bucket that was deleted
afterwards. My IAM user name is shown as `<iam-user>`.

```bash
aws s3api create-bucket --region ap-south-1 --bucket devops-hw18-24bcs10177-3cf8da \
  --create-bucket-configuration LocationConstraint=ap-south-1
aws s3api get-bucket-encryption --region ap-south-1 --bucket devops-hw18-24bcs10177-3cf8da \
  --query 'ServerSideEncryptionConfiguration.Rules[0].[ApplyServerSideEncryptionByDefault.SSEAlgorithm,BucketKeyEnabled]' \
  --output text
aws s3api get-public-access-block --region ap-south-1 --bucket devops-hw18-24bcs10177-3cf8da --output text
aws s3api get-bucket-ownership-controls --region ap-south-1 --bucket devops-hw18-24bcs10177-3cf8da --output text
```

```
{
    "Location": "http://devops-hw18-24bcs10177-3cf8da.s3.amazonaws.com/",
    "BucketArn": "arn:aws:s3:::devops-hw18-24bcs10177-3cf8da"
}
AES256	False
PUBLICACCESSBLOCKCONFIGURATION	True	True	True	True
RULES	BucketOwnerEnforced
```

A brand new bucket already has SSE-S3 encryption, all four Block Public Access
switches on, and ACLs disabled.

Versioning: upload twice, delete, then undo the delete.

```bash
aws s3api put-bucket-versioning --region ap-south-1 --bucket devops-hw18-24bcs10177-3cf8da \
  --versioning-configuration Status=Enabled
aws s3 cp --region ap-south-1 note.txt s3://devops-hw18-24bcs10177-3cf8da/notes/note.txt --no-progress
aws s3 cp --region ap-south-1 note.txt s3://devops-hw18-24bcs10177-3cf8da/notes/note.txt --no-progress
aws s3 rm --region ap-south-1 s3://devops-hw18-24bcs10177-3cf8da/notes/note.txt
aws s3api list-object-versions --region ap-south-1 --bucket devops-hw18-24bcs10177-3cf8da --prefix notes/ \
  --query '{versions:length(Versions),deleteMarkers:DeleteMarkers[].[VersionId,IsLatest]}'
aws s3api delete-object --region ap-south-1 --bucket devops-hw18-24bcs10177-3cf8da \
  --key notes/note.txt --version-id _Il2RavLpb9F4zndAFSINhL.jTMiMmAH
aws s3 cp --region ap-south-1 s3://devops-hw18-24bcs10177-3cf8da/notes/note.txt -
```

```
upload: ./note.txt to s3://devops-hw18-24bcs10177-3cf8da/notes/note.txt
upload: ./note.txt to s3://devops-hw18-24bcs10177-3cf8da/notes/note.txt
delete: s3://devops-hw18-24bcs10177-3cf8da/notes/note.txt
{
    "versions": 2,
    "deleteMarkers": [
        [
            "_Il2RavLpb9F4zndAFSINhL.jTMiMmAH",
            true
        ]
    ]
}
...
draft two
```

The delete only added a marker on top of both versions. Deleting the marker
brought the file back.

A bucket policy that denies any request where `aws:SecureTransport` is false.
The CLI always uses HTTPS, so I pointed it at the plain `http://` endpoint to
test it:

```bash
aws s3api put-bucket-policy --region ap-south-1 --bucket devops-hw18-24bcs10177-3cf8da \
  --policy file://deny-http.json
aws s3 cp --region ap-south-1 s3://devops-hw18-24bcs10177-3cf8da/notes/note.txt -
aws s3 ls --region ap-south-1 --endpoint-url http://s3.ap-south-1.amazonaws.com \
  s3://devops-hw18-24bcs10177-3cf8da/notes/
```

```
draft two

aws: [ERROR]: An error occurred (AccessDenied) when calling the ListObjectsV2 operation: User: arn:aws:iam::<account-id>:user/<iam-user> is not authorized to perform: s3:ListBucket on resource: "arn:aws:s3:::devops-hw18-24bcs10177-3cf8da" with an explicit deny in a resource-based policy
```

HTTPS works and HTTP is refused, even for my own broadly permitted user,
because an explicit deny beats any allow.

Deleting a versioned bucket is a gotcha. `aws s3 rb --force` failed with
`BucketNotEmpty ... You must delete all versions in the bucket`, because its
deletes only added more delete markers. I had to delete every version and
marker by ID with `delete-objects` first. Terraform's `force_destroy = true`
does that for you.
