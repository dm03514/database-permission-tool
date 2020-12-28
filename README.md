# database-permission-tool

Database permission tool (dpt) allows you to store your database roles permissions as configuration. 

# Quickstart - Configuring a Role

`dpt` models your entire database RBAC permission scheme as configuration. It requires a configuration file and the `database-permission-tool` CLI.

- Clone the repo:

```
$ git clone git@github.com:dm03514/database-permission-tool.git && cd database-permission-tool
```

- Install python requirements:

```
$ pip install -r requirements.txt
```

- Start Postgres:

```
$ docker-compose up -d
```

- Create a file to contain your permissions, and define your first role:

```
# permissions.yml

roles:
  - id: first_role
```

- Generate a plan, which shows you all the sql that `dpt` will execute:

```
$ python cmd/data-permission-tool.py plan --config=permissions.yml --db=postgres

DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'first_role') THEN

      CREATE GROUP first_role;
   END IF;
END
$do$;
```

- Apply the permissions:

```
$ python cmd/data-permission-tool.py apply --config=permissions.yml --db=postgres --connection-string='dbname=test user=test password=test host=localhost'

2020-12-27 20:22:48,497 - dpt.sources.postgres.postgres - INFO - Provisioning resource ROLE(first_role)
```

- Connect to postgres to view your new role!

```
$ psql -U test -h localhost
Password for user test:
psql (12.4, server 13.0 (Debian 13.0-1.pgdg100+1))
WARNING: psql major version 12, server major version 13.
         Some psql features might not work.
Type "help" for help.

test=# select * from pg_roles where rol
rolbypassrls    rolconfig       rolcreatedb     rolinherit      rolpassword     rolsuper
rolcanlogin     rolconnlimit    rolcreaterole   rolname         rolreplication  rolvaliduntil
test=# select * from pg_roles where rolname = 'first_role';
  rolname   | rolsuper | rolinherit | rolcreaterole | rolcreatedb | rolcanlogin | rolreplication | rolconnlimit | rolpassword | rolvaliduntil | rolbypassrls | rolconfig |  oid
------------+----------+------------+---------------+-------------+-------------+----------------+--------------+-------------+---------------+--------------+-----------+-------
 first_role | f        | t          | f             | f           | f           | f              |           -1 | ********    |               | f            |           | 16397
(1 row)
```
