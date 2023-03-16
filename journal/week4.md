# Week 4 — Postgres and RDS

# Required Homework
- [x] Watch Ashish's Week 4 - <a href="https://www.youtube.com/watch?v=UourWxz7iQg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=46">Securing Your Amazon RDS Postgres Database</a>
- [x] Create a RDS Postgres Instance - <a href="https://www.youtube.com/watch?v=EtD7Kv5YCUs&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=47">Live Stream</a>
- [x] Bash scripting for common database actions 
- [ ] Install Postgres Driver in Backend Application 
- [ ] Connect Gitpod to RDS Instance
- [ ] Create Cognito Trigger to insert user into database
- [ ] Create new activities with a database insert

# Homework Challenges
None assigned - leaving here in the event I think of any that I want to add to come back to after the bootcamp is finished or as time permits.
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]
- [ ]


# Securing AWS RDS Databases
## What type of Database is RDS?
<img src="./assets/week4/relational-nonrelational-db.jpg">

Relational Database (SQL)
- MySQL
- SQL Server
- Postgres

These have tables and rows within the tables.

Non-relational Database (NoSQL)
- dynamoDB

These databases are decoupled, there are no strong relationships between the columns and rows. 

## Creating RDS with Security in Mind
- Ensure you are in the appropriate region. 
- Master password: create a custom, more secure password
- Make sure encryption is enabled

Once the RDS instance is created, we'll look at some security best practices:
- Ensure the correct region is set
- Make sure the RDS instance is not publicly accessible
  - This may have to be edited to Publicly accessible, however make sure inbound security group rules are configured to ONLY allow the appropriate users on specific, allowed, IP ranges
- Check the security group rules:
  - Outbound rules can go anywhere 
  - Inbound rules, by default, only allow it to talk to itself
    - Security group may need to be edited/another rule may need to be added
    - Do NOT allow Source to be set to Anywhere, this will allow anyone anywhere to connect to the database
    - For working with a live organization, use custom, set the custom IP address range for the org, OR the VPN IP address that's been provided for all devs
- IAM privileges must be assigned to extend access the RDS database has to other resources in the cloud.
- For production environments: make sure to enable deletion protection & Multi-AZ 

If the database is no longer being used, it is best practice to delete the database.
- This will require you to confirm the deletion 


# Security Best Practices for Amazon RDS
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.Security.html
## AWS RDS Security Best Practices 
- Use VPCs: Use Amazon Virtual Private Cloud (VPC) to create a private network for your RDS instance. 
  - This helps prevent unauthorized access to your instance from the public internet.
- Compliance requirements that the organization must meet.
  - RDS Instances should only be in the AWS region that you are legally allowed to store user data in.
  - GDPR, ISO 27001, PCI DSS, etc. 
- Amazon Organizations SCP - manages RDS deletion, creation, region lock, enforce encryption, etc.
- AWS CloudTrail is enabled & monitored to trigger alerts based on malicious RDS behavior by an identity in AWS.
- Amazon Guardduty is enabled on the same account & region of RDS.

## Application RDS Security Best Practices
- RDS Instance should use appropriate authentication
  - Use IAM authentication, Kerberos, etc. 
  - Do NOT use the default
- Database User Lifecycle Management - Create, modify, & delete users
- AWS User Access Lifecycle Management - Change of roles, revoke roles, etc.
- Security groups should be restricted to only allow known IP addresses
- Do not allow RDS to be internet/publicly accessible
- Encryption for data in transit for comms between Apps & RDS
- Secret Management: Master user passwords can be used with AWS Secrets Manager to automatically rotate the secrets for Amazon RDS


# Amazon RDS Security
https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/UsingWithRDS.html




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
We can use the `createdb` command to create our database:

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

## Add a Universal Unique Identifier (UUID) Extension

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

<img src="./assets/week4/chmod-bin.jpg">



OR

```sh
chmod 644 bin/db-create
chmod 644 bin/db-drop
chmod 644 bin/db-schema-load
```

<img src="./assets/week4/permissions.png">

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

Run the following command

```sh
./bin/db-drop
```

After adding sed to `db-drop` the DB successfully dropped.

<img src="./assets/week4/db-drop.jpg">


# Add Shell Script to Create DB

Add the following in `db-create`

```sh
echo "db-create"

NO_DB_CONNECTION_URL=$(sed 's/\/cruddur//g' <<<"$CONNECTION_URL")
```

```sql
CREATE database cruddur;
```

Run the following command

```sh
./bin/db-create
```

<img src="./assets/week4/db-create.jpg">


# Add Shell Script to `db-schema-load`

```sh
echo "db-schema-load"

psql $CONNECTION_URL cruddur < db/schema.sql
```

<img src="./assets/week4/db-schema-load.jpg">


```
cd ..
./backend-flask/bin/db-schema-load
```

<img src="./assets/week4/db-schema-2.jpg">

The path is executing relative to where we are. 
- In order to get this to work with the current way `db-schema-load` is written, we would need to edit it slightly to be `backend-flask/db/schema.sql`. But we don't want this.
- We will need to use real path to find the `schema.sql` file

## Edit the `db-schema-load` file with the following:

```sh
$echo realpath

echo "db-schema-load"
psql $CONNECTION_URL cruddur < db/schema.sql
```

Try to execute the file again

```sh
./backend-flask/bin/db-schema-load
```


<img src="./assets/week4/realpath-nofile.jpg">



### Edit again, this time giving realpath a parameter

```sh
$echo realpath .

echo "db-schema-load"
psql $CONNECTION_URL cruddur < db/schema.sql
```

Try to execute the file again

```sh
./backend-flask/bin/db-schema-load
```

Same error occurred...

### Trying again but this time, wrapping realpath
```sh
$echo $(realpath .)

echo "db-schema-load"
psql $CONNECTION_URL cruddur < db/schema.sql
```

Try to execute the file again

```sh
./backend-flask/bin/db-schema-load
```

<img src="./assets/week4/realpath-wrapped.jpg">

```
cd backend-flask
./bin/db-schema-load
```

<img src="./assets/week4/realpath-wrapped-backend-flask.jpg">


- This time it worked


### Use `schema_path` to locate the file

```sh
schema_path = $(realpath ..)/db/schema.sql
echo $schema_path

echo "db-schema-load"
psql $CONNECTION_URL cruddur < db/schema.sql
```

<img src="./assets/week4/schema-load-uuid-exists.jpg">




```sh
echo "db-schema-load"

schema_path="$(realpath ..)/db/schema.sql"
echo $schema_path

psql $CONNECTION_URL cruddur < $schema_path
```

<img src="./assets/week4/schema_path.jpg">

The absolute path for `schema.sql` is listed:
- `/workspace/aws-bootcamp-cruddur-2023/db/schema.sql`

Only works from within `backend-flask`

<img src="./assets/week4/backend-flask-schema.jpg">


## To toggle between local and prod
In `db-schema-load` add the following & make the appropriate edits:

```sh
echo "ARG FIRST"
# echo $0 --- not needed
echo $1

echo "db-schema-load"
schema_path="$(realpath .)/db/schema.sql"
echo $schema_path

psql $CONNECTION_URL cruddur < db/schema.sql
```


Then run the following command

```sh
./bin/db-schema-load prod
```

<img src="./assets/week4/schema-load-arg-prod.jpg">

Using `$0` & `$1` didn't narrow down to what we expected which was just `prod`

<img src="./assets/week4/schema-load-echo1.jpg">

Removed `$0` and `$1` was the key to showing prod environment


## Add the following to `db-schema-load`

```sh
echo "db-schema-load"
schema_path="$(realpath .)/db/schema.sql"
echo $schema_path

if [ "$1" = "prod" ]; then
    echo "using production"
    CON_URL=$CONNECTION_URL
else
    CON_URL=$CONNECTION_URL
fi

psql $CON_URL cruddur < $schema_path
```


Then run the following

```sh
./bin/db-schema-load prod
```

<img src="./assets/week4/schema-using-prod.jpg">


# Print in Color

We we can make prints for our shell scripts coloured so we can see what we're doing:

https://stackoverflow.com/questions/5947742/how-to-change-the-output-color-of-echo-in-linux


```sh
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-schema-load"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"
```

# Create User and Activities Tables

https://www.postgresql.org/docs/current/sql-createtable.html

Think of these schemas as namespaces, by default they are set to public.
- Defining them as public out of good habit

```sql
DROP TABLE IF EXISTS public.users;
DROP TABLE IF EXISTS public.activities;
```

```sql
CREATE TABLE public.users (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  display_name text,
  handle text,
  cognito_user_id text,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```

```sql
CREATE TABLE public.activities (
  uuid UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  user_uuid UUID NOT NULL,
  message text NOT NULL,
  replies_count integer DEFAULT 0,
  reposts_count integer DEFAULT 0,
  likes_count integer DEFAULT 0,
  reply_to_activity_uuid integer,
  expires_at TIMESTAMP,
  created_at TIMESTAMP default current_timestamp NOT NULL
);
```

## Run Tables in CLI

```sh
./bin/db-schema-load
```


# Create `db-connect` in `/bin`

```sh
#! /usr/bin/bash

psql $CONNECTION_URL
```

## Change Permissions

Run the following:

```sh
chmod u+x ./bin/db-connect
```

## Test `db-connect`

```sh
./bin/db-connect

\dt
```

- Both tables should display in the CLI.


# Create `db-seed`

```sh
#! /usr/bin/bash 

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-seed"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

echo "db-schema-load"

seed_path="$(realpath .)/db/seed.sql"
echo $seed_path

if [ "$1" = "prod" ]; then
    echo "Running in production mode"
    CON_URL=$PROD_CONNECTION_URL
else
    CON_URL=$CONNECTION_URL
fi

psql $CON_URL cruddur < $seed_path
```

# Create `seed.sql`

```sql
INSERT INTO public.users (display_name, handle, cognito_user_id)
VALUES
  ('Andrew Brown', 'andrewbrown' ,'MOCK'),
  ('Andrew Bayko', 'bayko' ,'MOCK');

INSERT INTO public.activities (user_uuid, message, expires_at)
VALUES
  (
    (SELECT uuid from public.users WHERE users.handle = 'andrewbrown' LIMIT 1),
    'This was imported as seed data!',
    current_timestamp + interval '10 day'
  )
```


## Change Permissions

```sh
chmod u+x ./bin/db-seed
```

## Run `db-schema-load` then seed data

```sh
./bin/db-schema-load
./bin/db-seed
```

<img src="./assets/week4/seed-user-uuid-doesnt-exist.jpg">

Looking in the `schema.sql` file, we didn't define the user_uuid.

## Add `user_uuid` in `schema.sql`
Add the following under public.activities:

```sql
user_uuid UUID NOT NULL,
```

### Run the following commands to try seeding data again:

```sh
./bin/db-schema-load
./bin/db-seed
```

<img src="./assets/week4/seeded-data.jpg">

# Connect to the database
Run the following commands

```
./bin/db-connect
\dt
\x on
SELECT * FROM activities;
```

<img src="./assets/week4/db-connect-activities.jpg">

- Timestamps will present us with a challenge. 
  - Do we store them in UTC or in the local time zone?


Within Gitpod, open the Database Explorer on the left.
- Click onto the PostgreSQL tab
- Type in Cruddur for the Connection Name
- Host: 127.0.0.1
- Port: 5432
- Username: postgres
- Password
- Databases: postgres
- Then click Connect

<img src="./assets/week4/connect-to-db-server.jpg">

Try to drop the connection from the DB

<img src="./assets/week4/db-drop-cruddur.jpg">

We need to create a way to see active connections.

# Add Script to View Active Connections

```
NO_DB_URL=$(sed 's/\/cruddur//g' <<<"$URL")
psql $NO_DB_URL -c "select pid as process_id, \
       usename as user,  \
       datname as db, \
       client_addr, \
       application_name as app,\
       state \
from pg_stat_activity;"
```

We could have idle connections left open by our Database Explorer extension, try disconnecting and checking again the sessions

## Create `db-sessions` in `/bin`

```sql
#! /usr/bin/bash 

CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-sessions"
printf "${CYAN}== ${LABEL}${NO_COLOR}\n"

if [ "$1" = "prod" ]; then
    echo "Running in production mode"
    URL=$PROD_CONNECTION_URL
else
    RL=$CONNECTION_URL
fi

NO_DB_URL=$(sed 's/\/cruddur//g' <<<"$URL")
psql $NO_DB_URL -c "select pid as process_id, \
    usename as user,  \
    datname as db, \
    client_addr, \
    application_name as app,\
    state \
from pg_stat_activity;"
```


```
chmod u+x bin/db-sessions
```

<img src="./assets/week4/psql-error-connection-failed.jpg">

^^ hit the error above after not changing every variable to URL. After correcting this in `db-sessions` I was able to successfully display the active connections to my database.


<img src="./assets/week4/db-sessions-success.jpg">

Going back to database explorer
- Right click on the database
- Close connection

I was unable to terminate the active connection. 
### Troubleshooting Active Connections

- Attempting to do docker compose up again before trying to display the active connection again.

One session remains idle.
- Running docker compose down
- Running `./bin/db-sessions` to confirm the connections are no longer active
- Running docker compose up again 
- Running `./bin/db-sessions` to check active sessions and only one shows as active, as expected

<img src="./assets/week4/sessions-1.jpg">

Note: try to stay away from the Database Explorer section since it opens connections and doesn't properly close them out.


# Create `db-setup` & Add Scripts

```sql
#! /usr/bin/bash 
-e # stop if it fails at any point
CYAN='\033[1;36m'
NO_COLOR='\033[0m'
LABEL="db-setup"
printf "${CYAN}==== ${LABEL}${NO_COLOR}\n"

bin_path="$(realpath .)/bin"

source "$bin_path/db-drop"
source "$bin_path/db-create"
source "$bin_path/db-schema-load"
source "$bin_path/db-seed"
```

```
chmod u+x bin/db-setup
```

<img src="./assets/week4/db-setup.jpg">