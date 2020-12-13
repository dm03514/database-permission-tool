import networkx as nx


class Permissions:
    def __init__(self, graph):
        self.graph = graph

    # TODO - figure efficient lookups up after the POC

    def groups(self):
        return [n for n, attrs in self.graph.nodes(data=True)
                if attrs.get('type') == 'GROUP']

    def users(self):
        return [n for n, attrs in self.graph.nodes(data=True)
                if attrs.get('type') == 'USER']

    def users_of_group(self, group):
        edges = self.graph.edges(group, data=True)
        users = []
        for _, user, attrs in edges:
            if attrs['type'] == 'USER':
                users.append(user.id())
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

    for group in conf.get('groups', []):
        g = Group(_id=group['id'])
        Graph.add_node(g, **g.attrs())

        for user_id in group.get('users', []):
            u = users[user_id]
            Graph.add_edge(u, g, **u.attrs())

    return Permissions(graph=Graph)


class User:
    def __init__(self, _id):
        self._id = _id

    def id(self):
        return self._id

    def attrs(self):
        return {
            'id': self.id(),
            'type': 'USER'
        }


class Group:
    def __init__(self, _id):
        self._id = _id

    def id(self):
        return self._id

    def attrs(self):
        return {
            'id': self._id,
            'type': 'GROUP'
        }
