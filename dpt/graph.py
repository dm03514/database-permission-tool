import networkx as nx


class Permissions:
    def __init__(self, graph):
        self.graph = graph

    def groups(self):
        return [n for n, attrs in self.graph.nodes(data=True)
                if attrs['type'] == 'GROUP']


def new(conf):
    """
    new parses a permission config into a Permissions graph.

    :param conf:
    :return:
    """
    Graph = nx.Graph()
    for group in conf.get('groups', []):
        g = Group(name=group['name'])
        Graph.add_node(g, **g.attrs())
    return Permissions(graph=Graph)


class Group:
    def __init__(self, name):
        self.name = name

    def attrs(self):
        return {
            'name': self.name,
            'type': 'GROUP'
        }
