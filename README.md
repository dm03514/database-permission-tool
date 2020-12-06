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
# group.yml

groups:
  - name: test-group
  - name: test-group-2
```

- Plan the changes

```
$ python cmd/data-permission-tool.py plan --config=$(pwd)/examples/group.yml --db=postgres
CREATE GROUP test-group;
CREATE GROUP test-group-2;
```

- Apply the changes

```
$ python cmd/data-permission-tool.py plan --config=$(pwd)/examples/group.yml --db=postgres
```

