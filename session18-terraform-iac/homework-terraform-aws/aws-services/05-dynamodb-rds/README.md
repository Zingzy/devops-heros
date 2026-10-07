# DynamoDB and RDS: database services

DynamoDB is a serverless NoSQL key value store. RDS runs a normal relational
engine such as PostgreSQL for you. If I know the access patterns up front and
need steady speed at any scale, DynamoDB. If I need joins, ad hoc queries and
transactions across tables, RDS.

## DynamoDB

- **NoSQL.** No schema beyond the primary key, no joins, no SQL planner. Every
  read goes through a key, so a well designed table answers in milliseconds at
  any size. Fully managed and replicated across three AZs. Capacity is on-demand
  (pay per request, AWS's recommendation for most tables) or provisioned.
- **Tables.** A collection of items. Only the primary key is declared. Global
  secondary indexes add other query patterns (up to 20, any time), local ones
  must be created with the table.
- **Items.** One record, up to 400 KB. Items in one table can have completely
  different attributes.
- **Attributes.** A name and a typed value: string `S`, number `N` (sent as a
  string), binary `B`, `BOOL`, `NULL`, list `L`, map `M`, and sets.
- **Partition key.** Required. DynamoDB hashes it to pick the physical
  partition, and every `Query` must name one value of it. It needs many distinct,
  evenly used values, or one hot partition gets throttled.
- **Sort key.** Optional. Items with the same partition key are stored sorted by
  it, which allows range conditions such as `BETWEEN` and `begins_with`.
- **Use cases.** User profiles, sessions and carts, game state, IoT events keyed
  by device and time, and serverless apps on Lambda.

## RDS

- **Relational database.** AWS runs the engine on managed instances and handles
  provisioning, patching, backups and failover. I still own the schema, the SQL
  and the instance size, but get no OS access.
- **Supported engines.** Aurora (MySQL and PostgreSQL compatible), PostgreSQL,
  MySQL, MariaDB, Oracle, SQL Server and Db2.
- **DB instances.** An instance class plus storage. Classes look like EC2 types
  with a `db.` prefix, for example `db.t4g.micro`. Storage is EBS (`gp3`, `io2`)
  and can grow but never shrink. Instances sit in a DB subnet group spanning at
  least two AZs.
- **Security.** Private subnets with `PubliclyAccessible` off, a security group
  that only allows the app servers, KMS encryption at rest (chosen at creation),
  TLS in transit, the master password kept in Secrets Manager, optional IAM
  database authentication, and deletion protection.
- **Backups.** Automated daily snapshots plus transaction logs give point in time
  restore within the retention period of 1 to 35 days. Manual snapshots stay
  until deleted. A restore always creates a new instance.
- **Multi-AZ.** A synchronous standby in another AZ. If the primary fails, the
  DNS endpoint moves to the standby in about a minute or two. The standby serves
  no reads. Multi-AZ DB clusters add two readable standbys.
- **Read replicas.** Asynchronous copies with their own endpoints for scaling
  reads, up to 15 for MySQL, MariaDB and PostgreSQL, also cross region. A replica
  can be promoted to a standalone database.
- **Use cases.** The main database of a web app, anything needing transactions
  and joins (orders, payments), and moving an existing MySQL, Oracle or SQL Server
  database into AWS.

## Example: a DynamoDB table

Run on my account in `ap-south-1`. The table existed for about two minutes.

```bash
aws dynamodb create-table --region ap-south-1 --table-name devops-hw18-orders \
  --attribute-definitions AttributeName=customer_id,AttributeType=S AttributeName=order_date,AttributeType=S \
  --key-schema AttributeName=customer_id,KeyType=HASH AttributeName=order_date,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --tags Key=Project,Value=devops-homework Key=Session,Value=18 Key=Owner,Value=24bcs10177 \
  --query 'TableDescription.[TableName,TableStatus,BillingModeSummary.BillingMode]' --output text
aws dynamodb wait table-exists --region ap-south-1 --table-name devops-hw18-orders
aws dynamodb put-item --region ap-south-1 --table-name devops-hw18-orders --item \
  '{"customer_id":{"S":"c-101"},"order_date":{"S":"2026-10-02"},"total":{"N":"450"},"coupon":{"S":"DIWALI10"}}'
aws dynamodb query --region ap-south-1 --table-name devops-hw18-orders \
  --key-condition-expression 'customer_id = :c AND begins_with(order_date, :m)' \
  --expression-attribute-values '{":c":{"S":"c-101"},":m":{"S":"2026-10"}}' \
  --query 'Items[].[order_date.S,total.N,coupon.S]' --output text
```

```
devops-hw18-orders	CREATING	PAY_PER_REQUEST
2026-10-02	450	DIWALI10
```

Only the two key attributes were declared. I also put an order from September
and one for another customer. The query used the partition key and a
`begins_with` on the sort key to get just this customer's October orders.

Querying a non key attribute fails, and on real DynamoDB it first fails on a
reserved word, since `total` is one:

```bash
aws dynamodb query --region ap-south-1 --table-name devops-hw18-orders \
  --key-condition-expression 'total > :t' --expression-attribute-values '{":t":{"N":"100"}}'
```

```

aws: [ERROR]: An error occurred (ValidationException) when calling the Query operation: Invalid KeyConditionExpression: Attribute name is a reserved keyword; reserved keyword: total
```

With the name aliased as `#t` through `--expression-attribute-names`, the real
problem shows: `Query condition missed key schema element: customer_id`. A
`Query` always needs the partition key. Finding all orders over 100 needs a
`Scan` or a GSI.

Writing the same key again replaces the whole item:

```bash
aws dynamodb put-item --region ap-south-1 --table-name devops-hw18-orders --item \
  '{"customer_id":{"S":"c-101"},"order_date":{"S":"2026-10-02"},"total":{"N":"999"}}'
aws dynamodb get-item --region ap-south-1 --table-name devops-hw18-orders \
  --key '{"customer_id":{"S":"c-101"},"order_date":{"S":"2026-10-02"}}' --query 'Item'
aws dynamodb delete-table --region ap-south-1 --table-name devops-hw18-orders \
  --query 'TableDescription.TableStatus' --output text
```

```
{
    "total": {
        "N": "999"
    },
    "customer_id": {
        "S": "c-101"
    },
    "order_date": {
        "S": "2026-10-02"
    }
}
...
DELETING
```

`coupon` is gone. `update-item` changes single attributes instead.

## Example: RDS, catalogue only

An RDS instance takes 10 or more minutes to create, so I did not create one.
These calls only read what RDS offers in `ap-south-1`:

```bash
aws rds describe-db-engine-versions --region ap-south-1 --engine postgres --default-only \
  --query 'DBEngineVersions[].[Engine,EngineVersion,DBParameterGroupFamily]' --output text
aws rds describe-orderable-db-instance-options --region ap-south-1 --engine postgres --engine-version 17.6 \
  --db-instance-class db.t4g.micro \
  --query 'OrderableDBInstanceOptions[].[DBInstanceClass,StorageType,MultiAZCapable,ReadReplicaCapable,SupportsStorageEncryption,SupportsIAMDatabaseAuthentication]' \
  --output text
```

```
postgres	18.3	postgres18
db.t4g.micro	gp2	True	True	True	True
db.t4g.micro	gp3	True	True	True	True
db.t4g.micro	io1	True	True	True	True
db.t4g.micro	io2	True	True	True	True
```

A new PostgreSQL instance would default to 18.3. Even the smallest Graviton
class supports Multi-AZ, read replicas, encryption at rest and IAM
authentication on every storage type.
