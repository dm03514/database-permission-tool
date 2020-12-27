import os
import unittest

import yaml

from dpt import settings
from dpt.graph import new


class GraphTestCase(unittest.TestCase):

    def test_new_graph_with_users_correct_node_count(self):
        perms = new({
            'users': [
                {
                    'id': 'user_id_1'
                }
            ],
            'roles': [
                {
                    'id': 'new_group',
                    'members': [
                        {
                            'id': 'user_id_1',
                            'type': 'USER'
                        }
                    ]
                }
            ]
        })
        nodes = perms.graph.nodes(data=True)
        self.assertEqual(2, len(nodes), nodes)
        attrs = [attr for n, attr in nodes]
        self.assertEqual([
            {'id': 'user_id_1', 'type': 'USER'},
            {'id': 'new_group', 'type': 'ROLE'}
        ], attrs)

    def test_new_graph_policies(self):
        f = open(os.path.join(settings.EXAMPLES_DIR, 'role_permissions.yml'))
        conf = yaml.safe_load(f)
        perms = new(conf)
        nodes = perms.graph.nodes(data=True)
        attrs = [attr for n, attr in nodes]
        self.assertEqual([
            {'id': 'user_admin', 'type': 'USER'},
            {'id': 'user_reg', 'type': 'USER'},
            {'id': 'public', 'type': 'SCHEMA'},
            {'id': 'admin', 'type': 'ROLE'},
            {'id': 'readonly', 'type': 'ROLE'},
            {'id': 'admin', 'type': 'POLICY',
             'subject': {
                 'id': 'admin',
                 'type': 'ROLE'
             },
             'target': {
                 'id': 'public', 'type': 'SCHEMA'
             },
             'permissions': ['ALL']
             },
            {},
            {'id': 'readonly', 'type': 'POLICY', 'subject': {
                'id': 'readonly',
                'type': 'ROLE'
            },
            'target': {
                'id': 'public',
                'type': 'SCHEMA'
            },
             'permissions': ['SELECT']
             },
            {}
        ], attrs)
