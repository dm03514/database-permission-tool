import unittest

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
                    'users': [
                        'user_id_1'
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
