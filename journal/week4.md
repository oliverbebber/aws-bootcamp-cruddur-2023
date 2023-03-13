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
    --enable-performance-insights \
    --performance-insights-retention-period 7 \ 
    --no-deletion-protection
```
This will take about 10-15 mins

We can temporarily stop an RDS instance for 4 days when we aren't using it.


Notes: Master Password requirements: must be 8 characters long. RDS requirements are between 8-30 characters
- DO NOT SAVE THE PASSWORD IN THE FILE
- We can set this as an env var
- For enhanced security: Change the port to something other than 5432


Error occurred InvalidClientTokenID – the security token included in the request is invalid

More errors occurred while attempting to create my own RDS instance --- this appears to have been an issue due to the indention not being how it needed to be.

<img src="./assets/week4/aws-cli-rds.jpg">

<img src="./assets/week4/create-rds-instance.jpg">

Comment out DynamoDB in `docker-compose.yml` then run docker compose up

Go back into AWS RDS and check on the RDS instance.
- Click into the instance
- Click Actions
- Click Stop temporarily

Stopping the instance temporarily will result in the instance starting automatically after 7 days.

<img src="./assets/week4/rds-stop-temp.jpg">

# Connect to Postgres
To connect to psql via the psql client cli tool remember to use the host flag to specific localhost.

```
psql -Upostgres --host localhost
```

Common PSQL commands:

```sql
\x on -- expanded display when looking at data
\q -- Quit PSQL
\l -- List all databases
\c database_name -- Connect to a specific database
\dt -- List all tables in the current database
\d table_name -- Describe a specific table
\du -- List all users and their roles
\dn -- List all schemas in the current database
CREATE DATABASE database_name; -- Create a new database
DROP DATABASE database_name; -- Delete a database
CREATE TABLE table_name (column1 datatype1, column2 datatype2, ...); -- Create a new table
DROP TABLE table_name; -- Delete a table
SELECT column1, column2, ... FROM table_name WHERE condition; -- Select data from a table
INSERT INTO table_name (column1, column2, ...) VALUES (value1, value2, ...); -- Insert data into a table
UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition; -- Update data in a table
DELETE FROM table_name WHERE condition; -- Delete data from a table
```

MySQL doesn’t use \q – just q

Enter the following into the CLI to list the databases postgres template0 and template1 should display
```
\l
```

<img src="./assets/week4/list-dbs.jpg">

# Create (and dropping) our database
We can use the createdb command to create our database:

https://www.postgresql.org/docs/current/app-createdb.html

```
createdb cruddur -h localhost -U postgres
```

```sh
psql -U postgres -h localhost
```

```sql
\l
DROP database cruddur;
```

We can create the database within the PSQL client

```sql
CREATE database cruddur;
```

<img src="./assets/week4/cruddur-db.jpg">


# Add Schema file 

We'll create a new SQL file called `schema.sql`
and we'll place it in `backend-flask/db`

# Add a Universal Unique Identifier (UUID) Extension

We are going to have Postgres generate out UUIDs.
We'll need to use an extension called:

```sql
CREATE EXTENSION "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

Postgres comes with some extensions to turn on.
- Make sure these extensions are available on AWS.

# Import Script

The command to import:

```
cd backend-flask
psql cruddur < db/schema.sql -h localhost -U postgres
```

<img src="./assets/week4/create-extension.jpg">

# Make a new connection_url string
Test the connection_url by typing in:

```sh
psql postgresql://postgres:password@localhost:5432/cruddur
```

Successfully connected to postgres DB without having to enter the password in.

<img src="./assets/week4/test-connection-url.jpg">

## Set env var

```sh
\q
export CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
psql $CONNECTION_URL
```

<img src="./assets/week4/env-var.jpg">

## Set GitPod Env Var

```sh
\q
gp env CONNECTION_URL="postgresql://postgres:password@localhost:5432/cruddur"
```

<img src="./assets/week4/gp-env.jpg">

## Set Production & GitPod Env Var

Set aside

```sh
export PROD_CONNECTION_URL="postgresql://masterusername:masterpassword@cruddur-db-instance.endpoint.amazonaws.com:5432/cruddur"
gp env PROD_CONNECTION_URL="postgresql://masterusername:masterpassword@cruddur-db-instance.endpoint.amazonaws.com:5432/cruddur"
```

<img src="./assets/week4/prod-env-vars.jpg">


# Create `bin` folder w/create `db-create`, `db-drop`, & `db-schema-load`
In the backend-flask directory, create these folders and files without extensions.

```sh
mkdir /workspace/aws-bootcamp-cruddur-2023/backend-flask/bin
```

Within these files, we need to run a bash script.
- Before adding the shebang to the files, we need to find where bash is.

Run the following command:

```sh
whereis bash
```

# Add Shell Script to Drop the DB
`bin/db-drop`

```sh
#! /usr/bin/bash

psql $CONNECTION_URL -c "DROP database cruddur;"
```

Before we can run this, we need to give it permission otherwise running the following will result in "Permission denied"

```sh
./bin/db-create
```

```sh
ls -l ./bin
```

<img src="./assets/week4/current-bin-permissions.jpg">

r= read

w= write

x= executable

## Change permissions in scope of the user
We want to allow these files to become executable 

```sh
chmod u+x bin/db-create
chmod u+x bin/db-drop
chmod u+x bin/db-schema-load
```

OR

```sh
chmod 644 bin/db-create
chmod 644 bin/db-drop
chmod 644 bin/db-schema-load
```

<img src="./assets/week4/chmod-bin.jpg">


## Drop DB

```sh
./bin/db-drop
```

This resulted in an error due to us being currently connected to the open database.

<img src="./assets/week4/cannot-drop-open-DB.jpg">

Our CONNECTION_URL needs to exclude the database name.
- To do this in bash, we can use a tool called sed to manipulate text in place.
- This tool doesn't always work the same way in every linux system.


### Edit `db-drop` using sed

```sh
echo "db-drop"
# sed allows us to manipulate strings
# s = substitute
# what do we want to select - in the first / /
# what do we want to replace it with in the 2nd / /
# \ will escape the / that we want to replace
# g = global, which means that all matching occurrences in the line would be replaced
NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")

psql $NO_DB_CONNECTION_URL -c "DROP database cruddur;"
```


```sh
./bin/db-drop
```

After adding sed to `db-drop` the DB successfully dropped.

<img src="./assets/week4/db-drop.jpg">


# Add Shell Script to Create DB

Add the following in `db-create`

```sh
echo "db-create"
```

```sql
CREATE database cruddur;
```