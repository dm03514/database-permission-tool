import os

import psycopg2
import psycopg2.extras

from dpt import settings

current_dir = os.path.dirname(os.path.abspath(__file__))


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
        print('\n'.join(plan))
        # Add parameter bindings
        for statement in plan:
            # group table parameter binding is adding single quotes to the query
            # which is invalid. The group name should either be double quoted
            # or no quotes :(
            cursor.execute(statement)

        self.conn.commit()
        cursor.close()

    def plan(self):
        """
        Plan returns the SQL necessary to persist the graph into Postgres.

        :return:
        """
        # build all the groups statements
        sql_statements = []
        with open(os.path.join(settings.POSTGRES_SQL_DIR, 'create_role.sql')) as f:
            group_template = f.read()

        with open(os.path.join(settings.POSTGRES_SQL_DIR, 'add_user_to_group.sql')) as f:
            add_user_to_group_template = f.read()

        for role in self.perms.roles():
            sql_statements.append(
                group_template.format(role.id(), role.id())
            )
            for user_id in self.perms.users_of_role(role):
                sql_statements.append(
                    add_user_to_group_template.format(
                        role.id(),
                        user_id,
                    )
                )

        return sql_statements
