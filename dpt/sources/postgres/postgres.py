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
        with open(os.path.join(settings.POSTGRES_SQL_DIR, 'create_group.sql')) as f:
            group_template = f.read()

        for group in self.perms.groups():
            sql_statements.append(
                group_template.format(group.name, group.name)
            )

        return sql_statements
