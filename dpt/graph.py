from abc import ABC, abstractmethod
from collections import namedtuple

import networkx as nx


TYPE = namedtuple('Types', [
    'UNKNOWN',
    'USER',
    'SCHEMA',
    'ROLE',
    'POLICY',
    'SUBJECT',
    'TARGET',
    'PERMISSION',
])(
    UNKNOWN='UNKNOWN',
    USER='USER',
    SCHEMA='SCHEMA',
    ROLE='ROLE',
    POLICY='POLICY',
    SUBJECT='SUBJECT',
    TARGET='TARGET',
    PERMISSION='PERMISSION',
)


class Permissions:
    def __init__(self, graph):
        self.graph = graph

    # TODO - figure efficient lookups up after the POC

    def roles(self):
        return [n for n, attrs in self.graph.nodes(data=True)
                if attrs.get('type') == TYPE.ROLE]

    def users(self):
        return [n for n, attrs in self.graph.nodes(data=True)
                if attrs.get('type') == TYPE.USER]

    def policies(self):
        return [n for n, attrs in self.graph.nodes(data=True)
                if attrs.get('type') == TYPE.POLICY]

    def users_of_role(self, role):
        edges = self.graph.edges(role, data=True)
        users = []
        for _, user, attrs in edges:
            if attrs['type'] == TYPE.USER:
                users.append(user)
        return users


def new(conf):
    """
    new parses a permission config into a Permissions graph.

    :param conf:
    :return:
    """
    Graph = nx.Graph()

    users = {}
    schemas = {}
    roles = {}

    for user in conf.get('users', []):
        u = Resource(
            _id=user['id'],
            _type=TYPE.USER,
        )
        Graph.add_node(u, **u.attrs())
        users[u.id()] = u

    for schema in conf.get('schemas', []):
        s = Resource(
            _id=schema['id'],
            _type=TYPE.SCHEMA
        )
        Graph.add_node(s, **s.attrs())
        schemas[s.id()] = s

    for role in conf.get('roles', []):
        rl = Resource(
            _id=role['id'],
            _type=TYPE.ROLE,
        )
        roles[rl.id()] = rl
        Graph.add_node(rl, **rl.attrs())

        for user in role.get('users', []):
            u = users[user['id']]
            Graph.add_edge(u, rl, **u.attrs())

    for pc in conf.get('policies', []):
        subject = pc['subject']
        target = pc['target']
        # permissions = pc['permissions']

        policy = Policy(
            _id=pc['id'],
            subject=pc['subject'],
            target=pc['target'],
            permissions=pc['permissions'],
        )

        Graph.add_node(policy, **policy.attrs())

        if subject['type'] == TYPE.ROLE:
            rl = roles[subject['id']]
            Graph.add_edge(policy, rl, **{'type': TYPE.SUBJECT})
        else:
            raise NotImplementedError

        if target['type'] == TYPE.SCHEMA:
            schema = schemas[target['id']]
            Graph.add_edge(policy, schema, **{'type': TYPE.TARGET})
        else:
            raise NotImplementedError

        '''
        for perm in permissions:
            Graph.add_edge(policy, perm, **{'type': TYPE.PERMISSION})
        '''

    return Permissions(graph=Graph)


class R(ABC):

    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def id(self):
        pass


class Resource(R):
    def __init__(self, _id, _type=TYPE.UNKNOWN):
        self._id = _id
        self._type = _type

    def id(self):
        return self._id

    def type(self):
        return self._type

    def attrs(self):
        return {
            'id': self.id(),
            'type': self.type()
        }

    def __repr__(self):
        return 'Resource(_id="{}", _type="{}")'.format(
            self.id(),
            self.type(),
        )


class Policy(R):
    def __init__(self, _id, subject, target, permissions, _type=TYPE.POLICY):
        self._id = _id
        self._type = _type
        self.subject = subject
        self.target = target
        self.permissions = permissions

    def id(self):
        return self._id

    def type(self):
        return self._type

    def attrs(self):
        return {
            'id': self.id(),
            'type': self.type(),
            'subject': self.subject,
            'target': self.target,
            'permissions': self.permissions,
        }

    def __repr__(self):
        return 'Policy(_id="{}", _type="{}")'.format(
            self.id(),
            self.type(),
        )
