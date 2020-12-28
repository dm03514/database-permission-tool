import os

import psycopg2
import yaml

from dpt import settings


def export(connection_string):
    conn = psycopg2.connect(connection_string)

    with open(os.path.join(settings.REDSHIFT_SQL_DIR, 'list_groups.sql')) as f:
        list_groups = f.read()

    with open(os.path.join(settings.REDSHIFT_SQL_DIR, 'list_user_groups.sql')) as f:
        list_user_groups = f.read()

    conf = {
        'users': [],
        'schemas': [],
        'roles': [],
        'policies': []
    }

    cursor = conn.cursor(
        cursor_factory=psycopg2.extras.DictCursor
    )
    cursor.execute(list_groups)
    rows = cursor.fetchall()
    db_roles = {r['groname']: [] for r in rows}

    cursor.execute(list_user_groups)
    rows = cursor.fetchall()
    for row in rows:
        db_roles[row['groname']].append(row['usename'])

    cursor.close()
    for role, users in db_roles.items():
        conf['roles'].append({
            'id': role,
            'members': sorted(users)
        })

    conf['users'] = sorted(users)
    print(yaml.dump(conf))


