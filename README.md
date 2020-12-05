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
