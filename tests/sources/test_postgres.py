import os
import unittest

import yaml

from dpt import settings
from dpt.graph import new
from dpt.sources import postgres


class PostgresSQLTestCase(unittest.TestCase):

    def test_role_sql_is_correct(self):
        f = open(os.path.join(settings.EXAMPLES_DIR, 'role.yml'))
        conf = yaml.safe_load(f)
        perms = new(conf)
        postgres_perms = postgres.new(perms)
        plan = postgres_perms.plan()
        sql = [x.sql for x in plan]
        self.assertEqual([
            '''DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'test_group') THEN

      CREATE GROUP test_group;
   END IF;
END
$do$;''',
            '''DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'test_group_2') THEN

      CREATE GROUP test_group_2;
   END IF;
END
$do$;'''
        ], sql)

    def test_add_users_to_role_sql_is_correct(self):
        f = open(os.path.join(settings.EXAMPLES_DIR, 'add_users_to_role.yml'))
        conf = yaml.safe_load(f)
        perms = new(conf)
        postgres_perms = postgres.new(perms)
        plan = postgres_perms.plan()
        sql = [x.sql for x in plan]
        self.assertEqual([
            '''DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'test_group') THEN

      CREATE GROUP test_group;
   END IF;
END
$do$;''',
            '''ALTER GROUP test_group ADD USER user1;'''
        ], sql)

    def test_role_permissions_sql_is_correct(self):
        f = open(os.path.join(settings.EXAMPLES_DIR, 'role_permissions.yml'))
        conf = yaml.safe_load(f)
        perms = new(conf)
        postgres_perms = postgres.new(perms)
        plan = postgres_perms.plan()
        sql = [x.sql for x in plan]
        self.assertEqual([
            '''DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'admin') THEN

      CREATE GROUP admin;
   END IF;
END
$do$;''',
            'ALTER GROUP admin ADD USER user_admin;',
            '''DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_catalog.pg_roles
      WHERE rolname = 'readonly') THEN

      CREATE GROUP readonly;
   END IF;
END
$do$;''',
            'ALTER GROUP readonly ADD USER user_reg;',
            '\nGRANT ALL ON SCHEMA public TO admin;\n\n',
            'GRANT SELECT ON ALL TABLES IN SCHEMA public TO readonly;'
        ], sql)
