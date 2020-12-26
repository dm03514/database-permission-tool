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

        for member in role.get('members', []):
            if member['type'] == TYPE.USER:
                u = users[member['id']]
                Graph.add_edge(u, rl, **u.attrs())
            else:
                raise NotImplementedError

    for policy in conf.get('policies', []):
        p = Policy(
            _id=policy['id'],
            subject=policy['subject'],
            target=policy['target'],
            permissions=policy['permissions'],
        )

        Graph.add_node(p, **p.attrs())

        if policy['subject']['type'] == TYPE.ROLE:
            rl = roles[policy['subject']['id']]
            Graph.add_edge(p, rl, type=TYPE.SUBJECT)
        else:
            raise NotImplementedError

        if policy['target']['type'] == TYPE.SCHEMA:
            schema = schemas[policy['target']['id']]
            Graph.add_edge(p, schema, type=TYPE.TARGET)
        else:
            raise NotImplementedError

        for perm in policy['permissions']:
            Graph.add_edge(p, perm, type=TYPE.PERMISSION)

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
