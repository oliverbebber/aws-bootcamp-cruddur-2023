# Week 4 — Postgres and RDS

# Required Homework
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]

# Homework Challenges
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]

# Provision RDS Instance

Add this code into the CLI to create the instance

```
aws rds create-db-instance \
  --db-instance-identifier cruddur-db-instance \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version  14.6 \
  --master-username root \
  --master-user-password huEE33z2Qvl383 \
  --allocated-storage 20 \
  --availability-zone ca-central-1a \
  --backup-retention-period 0 \
  --port 5432 \
  --no-multi-az \
  --db-name cruddur \
  --storage-type gp2 \
  --publicly-accessible \
  --storage-encrypted \
  --no-deletion-protection
```
This will take about 10-15 mins

We can temporarily stop an RDS instance for 4 days when we aren't using it.


Notes: Master Password requirements: must be 8 characters long. RDS requirements are between 8-30 characters
- DO NOT SAVE THE PASSWORD IN THE FILE
- We can set this as an env var
- For enhanced security: Change the port to something other than 5432


Error occurred InvalidClientTokenID – the security token included in the request is invalid
