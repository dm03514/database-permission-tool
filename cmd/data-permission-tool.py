import argparse
import logging

import yaml
import networkx as nx

from dpt.sources import postgres, redshift
from dpt import graph

from dpt.logger import init

init(level='DEBUG')

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description='Manage database permissions'
    )
    parser.add_argument(
        'operation',
        type=str,
        choices=('apply', 'plan', 'graph', 'export'),
        help='dpt operation to perform')
    parser.add_argument(
        '--db',
        type=str,
        choices=('postgres', 'redshift'),
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

    if cli_args.operation == 'export':
        raise NotImplementedError
        '''
        if cli_args.db == 'redshift':
            redshift.export(cli_args.connection_string)
        else:
        return
        '''

    # load the config file
    conf = None
    with open(cli_args.config, 'r') as stream:
        try:
            conf = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)

    # parse the config file into a dpt graph
    perms = graph.new(conf)

    if cli_args.operation == 'graph':
        pdot = nx.drawing.nx_pydot.to_pydot(perms.graph)
        name = 'build/{}.png'.format('out')
        print('saving graph: "{}"'.format(name))
        pdot.write_png(name)
        return

    if cli_args.db == 'postgres':
        postgres_perms = postgres.new(
            perms,
            cli_args.connection_string,
        )
        if cli_args.operation == 'plan':
            print('\n\n'.join(stmnt.sql for stmnt in postgres_perms.plan()))
        elif cli_args.operation == 'apply':
            postgres_perms.apply()
        else:
            raise NotImplementedError


if __name__ == '__main__':
    main()
