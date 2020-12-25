from abc import ABC, abstractmethod

import networkx as nx


class Permissions:
    def __init__(self, graph):
        self.graph = graph

    # TODO - figure efficient lookups up after the POC

    def roles(self):
        return [n for n, attrs in self.graph.nodes(data=True)
                if attrs.get('type') == 'ROLE']

    def users(self):
        return [n for n, attrs in self.graph.nodes(data=True)
                if attrs.get('type') == 'USER']

    def users_of_role(self, role):
        edges = self.graph.edges(role, data=True)
        users = []
        for _, user, attrs in edges:
            if attrs['type'] == 'USER':
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

    for user in conf.get('users', []):
        u = User(_id=user['id'])
        Graph.add_node(u, **u.attrs())
        users[u.id()] = u

    for role in conf.get('roles', []):
        rl = Role(_id=role['id'])
        Graph.add_node(rl, **rl.attrs())

        for member in role.get('members', []):
            if member['type'] == 'USER':
                u = users[member['id']]
                Graph.add_edge(u, rl, **u.attrs())
            else:
                raise NotImplementedError

    return Permissions(graph=Graph)


class Resource(ABC):

    @abstractmethod
    def type(self):
        pass

    @abstractmethod
    def id(self):
        pass


class User(Resource):
    def __init__(self, _id):
        self._id = _id

    def id(self):
        return self._id

    def type(self):
        return 'USER'

    def attrs(self):
        return {
            'id': self.id(),
            'type': self.type()
        }


class Role(Resource):
    def __init__(self, _id):
        self._id = _id

    def id(self):
        return self._id

    def type(self):
        return 'ROLE'

    def attrs(self):
        return {
            'id': self._id,
            'type': self.type()
        }
