import os

current_dir = os.path.dirname(os.path.abspath(__file__))

POSTGRES_SQL_DIR = os.path.join(current_dir, 'sources', 'postgres', 'sql')
REDSHIFT_SQL_DIR = os.path.join(current_dir, 'sources', 'redshift', 'sql')
EXAMPLES_DIR = os.path.join(current_dir, '..', 'examples')
