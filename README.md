# database-permission-tool
Manage your database permissions in code 

Database permission tool (dpt) allows you to store your database roles permissions and resources as code.

What dpt does:
- Store your permissions and RBAC as code
- Persist changes in code to your database permission model (similiar to terraform)
- Query permissions to see which permissions a user has
- Import your database permissions into dpt 


What dpt doesn't do:
- Create resources other than permissions and roles 
  - dpt doesn't create tables or users



How do you manage your permissions? 

Many orgs I've worked for manually manages permissions by hand. Tools like Hashicorp Vault have heavy learning curves. Other organizations model permissions as sql statements and a migration tool using flyway. 

Datbase Permission Tool makes permissions and roles a first class citizen. It provides the same benefits for roles and permissions that terraform provides for infrstatructure.

# Examples


## Creating Groups

dpt is a CLI tool. It requires a permissions config definition and the database-permission-tool cli command. The following example creates 2 groups. Running the example requires that you have database-permission-tool repo cloned and docker-compose. 

- Start Postgres

```
$ docker-compose up -d
```

- Define a configuration file

```
# role.yml

roles:
  - id: test-group
  - id: test-group-2
```

- Plan the changes

```
$ python cmd/data-permission-tool.py plan --config=$(pwd)/examples/role.yml --db=postgres

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE rolname = 'test_group') THEN

      CREATE GROUP test_group;
   END IF;
END
$do$;

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE rolname = 'test_group_2') THEN

      CREATE GROUP test_group_2;
   END IF;
END
$do$;
```

- Apply the changes

```
$ python cmd/data-permission-tool.py apply --config=$(pwd)/examples/role.yml --db=postgres --connection-string='dbname=test user=test password=test host=localhost'

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE rolname = 'test_group') THEN

      CREATE GROUP test_group;
   END IF;
END
$do$;

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE rolname = 'test_group_2') THEN

      CREATE GROUP test_group_2;
   END IF;
END
$do$;
```

- View the roles in postgres
```
$ psql -U test -h localhost
Password for user test:
psql (12.4, server 13.0 (Debian 13.0-1.pgdg100+1))
WARNING: psql major version 12, server major version 13.
         Some psql features might not work.
Type "help" for help.

test=# select * from pg_roles;
          rolname          | rolsuper | rolinherit | rolcreaterole | rolcreatedb | rolcanlogin | rolreplication | rolconnlimit | rolpassword | rolvaliduntil | rolbypassrls | rolconfig |  oid
---------------------------+----------+------------+---------------+-------------+-------------+----------------+--------------+-------------+---------------+--------------+-----------+-------
...
test_group_2              | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           | 16390
test_group                | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           | 16385
```

# Workflow: Add Users To a Group

Users are not managed as part of permission tool. This means that users must be created outside of
the permission tool flow. 

- Create a user:

```
test=# CREATE USER user1;
CREATE ROLE
```

- Define configuration file

```
# add_users_to_role.yml

users:
  - id: user1

roles:
  - id: test_group
    users:
      - user1
```

- Plan

```
$ python cmd/data-permission-tool.py plan --config=$(pwd)/examples/add_users_to_role.yml --db=postgres
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE rolname = 'test_group') THEN

      CREATE GROUP test_group;
   END IF;
END
$do$;

ALTER GROUP test_group ADD USER user1;
```

- Apply

```
$ python cmd/data-permission-tool.py apply --config=$(pwd)/examples/add_users_to_role.yml --db=postgres --connection-string='dbname=test user=test password=test host=localhost'
DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles  -- SELECT list can be empty for this
      WHERE rolname = 'test_group') THEN

      CREATE GROUP test_group;
   END IF;
END
$do$;

ALTER GROUP test_group ADD USER user1;
```

- Verify that the user was added to the group

```
$ psql -U test -h localhost
Password for user test:
psql (12.4, server 13.0 (Debian 13.0-1.pgdg100+1))
WARNING: psql major version 12, server major version 13.
         Some psql features might not work.
Type "help" for help.

test=# select rolname from pg_user
test-# join pg_auth_members on (pg_user.usesysid=pg_auth_members.member)
test-# join pg_roles on (pg_roles.oid=pg_auth_members.roleid)
test-# where
test-# pg_user.usename='user1';
  rolname
------------
 test_group
(1 row)
```

# Test User Role Membership

# Workflow: Adding Permission to a Schema

# Workflow: Adding a New Table

# Test Table Access Permissions



