# database-permission-tool

Database permission tool (dpt) allows you to store your database roles permissions as configuration. 

# Quickstart - Configuring a Role

- Clone the repo:

```
$ git@github.com:dm03514/database-permission-tool.git
```

- Install python requirements:

```
$ pip install -r requirements.txt
```

- Start Postgres:

```
$ docker-compose up -d
```

- Create a file to contain your permissions. And define your first role:

```
# permissions.yml

roles:
  - id: first_role
```
