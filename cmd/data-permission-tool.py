import argparse

import yaml
import networkx as nx

from dpt.sources import postgres
from dpt import graph

def main():
    parser = argparse.ArgumentParser(
        description='Manage database permissions'
    )
    parser.add_argument(
        'operation',
        type=str,
        choices=('apply', 'plan'),
        help='dpt operation to perform')
    parser.add_argument(
        '--db',
        type=str,
        choices=('postgres',),
        help='target database system')
    parser.add_argument(
        '--connection-string',
        type=str,
        help='db connection string')
    parser.add_argument(
        '--config',
        type=str,
        help='config file')
    cli_args = parser.parse_args()

    # load the config file
    conf = None
    with open(cli_args.config, 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # parse the config file into a dpt graph
    perms = graph.new(conf)

    if cli_args.db == 'postgres':
        postgres_perms = postgres.new(
            perms,
            cli_args.connection_string,
        )
        if cli_args.operation == 'plan':
            print('\n'.join(postgres_perms.plan()))
        elif cli_args.operation == 'apply':
            postgres_perms.apply()


if __name__ == '__main__':
    main()
