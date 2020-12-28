import logging
import os

import psycopg2
import psycopg2.extras
from jinja2 import Template

from dpt import settings
from dpt.statement import Statement

current_dir = os.path.dirname(os.path.abspath(__file__))


logger = logging.getLogger(__name__)


def new(perms, connection_string=None):
    conn = None
    if connection_string is not None:
        conn = psycopg2.connect(connection_string)
    return Postgres(perms, conn)


class Postgres:
    def __init__(self, perms, conn=None):
        self.conn = conn
        self.perms = perms

    def apply(self):
        plan = self.plan()
        cursor = self.conn.cursor(
            cursor_factory=psycopg2.extras.DictCursor
        )
        # print('\n'.join(plan))
        # Add parameter bindings
        for statement in plan:
            # group table parameter binding is adding single quotes to the query
            # which is invalid. The group name should either be double quoted
            # or no quotes :(
            logger.debug(statement.sql)
            logger.info('Provisioning resource {}({})'.format(
                statement.resource.type(),
                statement.resource.id(),
            ))
            cursor.execute(statement.sql)
        self.conn.commit()
        cursor.close()

    def plan(self):
        """
        Plan returns the SQL necessary to persist the graph into Postgres.

        :return:
        """
        # build all the groups statements
        sql_statements = []
        # TODO add a jinja template loader
        with open(os.path.join(settings.POSTGRES_SQL_DIR, 'create_role.sql')) as f:
            role_template = f.read()

        with open(os.path.join(settings.POSTGRES_SQL_DIR, 'add_user_to_role.sql')) as f:
            add_user_to_role_template = f.read()

        with open(os.path.join(settings.POSTGRES_SQL_DIR, 'grant_on_schema.sql')) as f:
            grant_on_schema_template = f.read()

        with open(os.path.join(settings.POSTGRES_SQL_DIR, 'grant_select_schema.sql')) as f:
            grant_select_schema_template = f.read()

        with open(os.path.join(settings.POSTGRES_SQL_DIR, 'grant_default_privileges.sql')) as f:
            grant_default_privileges_template = f.read()

        for role in self.perms.roles():
            t = Template(role_template)
            sql_statements.append(
                Statement(
                    resource=role,
                    sql=t.render(
                        role_id=role.id(),
                    )
                )
            )

            for user in self.perms.users_of_role(role):
                t = Template(add_user_to_role_template)
                sql_statements.append(
                    Statement(
                        resource=user,
                        sql=t.render(
                            role_id=role.id(),
                            user_id=user.id(),
                        )
                    )
                )

        for policy in self.perms.policies():
            if policy.permissions.get('all') or policy.permissions.get('usage'):
                t = Template(grant_on_schema_template)
                sql_statements.append(
                    Statement(
                        resource=policy,
                        sql=t.render(
                            permission=policy.permissions,
                            target=policy.target,
                            subject=policy.subject
                        )
                    )
                )

            if policy.permissions.get('select'):
                t = Template(grant_select_schema_template)
                sql_statements.append(
                    Statement(
                        resource=policy,
                        sql=t.render(
                            target=policy.target,
                            subject=policy.subject
                        )
                    )
                )

            if policy.permissions.get('default_privileges'):
                t = Template(grant_default_privileges_template)
                sql_statements.append(
                    Statement(
                        resource=policy,
                        sql=t.render(
                            target=policy.target,
                            subject=policy.subject
                        )
                    )
                )

        return sql_statements
