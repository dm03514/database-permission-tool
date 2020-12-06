import os

from dpt import settings

current_dir = os.path.dirname(os.path.abspath(__file__))


class Postgres:
    def __init__(self, perms):
        self.perms = perms

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
            sql_statements.append(group_template % group.name)

        return sql_statements
