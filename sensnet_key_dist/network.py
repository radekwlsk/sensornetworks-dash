from secrets import randbits, randbelow
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go

from sensnet_key_dist.node import Node


class SensorNetwork:

    def __init__(self, n, k, s, x, r):
        """
        SensorNetwork represents the sensor network using Chan, Perrig, Song key distribution scheme
        :param n: number of nodes
        :param k: number of randomly selected keys stored in each node
        :param s: size of key pool
        :param x: grid dimension
        :param r: node's range in manhattan distance
        """
        assert 0 < k <= s
        assert n > 0
        self.n = n
        self.k = k
        self.x = x
        self.r = r
        self.key_pool = {i: randbits(64) for i in range(s)}
        self.nodes = dict()
        self.edges = set()
        self.components = list()
        self.graph = None

        for i in range(n):
            self.nodes.update(
                {i: Node(i,
                         keys={i: self.key_pool[i] for i in np.random.choice(s, self.k, replace=False)},
                         coords=(randbelow(self.x), randbelow(self.x)))}
            )

        for node in self.nodes.values():
            for other in self.nodes.values():
                if other.id != node.id and node.in_range(other, self.r):
                    node.establish_shared_keys(other)

        for node in self.nodes.values():
            self.add_edges(node)

        self.find_components()

        total_edges = self.n * (self.n - 1) / 2
        self.direct_coverage = len(self.edges) / total_edges

        self.coverage = max([len(c) for c in self.components]) / self.n

    def add_edges(self, node):
        for neighbour in node.neighbours:
            self.edges.add((node.id, neighbour) if node.id < neighbour else (neighbour, node.id))

    def find_components(self):
        def dfs(start):
            visited, stack = set(), [start]
            while stack:
                vertex = stack.pop()
                if vertex not in visited:
                    visited.add(vertex)
                    for (a, b) in self.edges:
                        if vertex == a and b not in visited:
                            stack.append(b)
                        elif vertex == b and a not in visited:
                            stack.append(a)
            return visited

        self.components = list()
        for node in self.nodes:
            for component in self.components:
                if node in component:
                    break
            component = dfs(node)
            if component not in self.components:
                self.components.append(component)

    def create_graph(self):
        nodes = go.Scatter(
            x=[n.x for n in self.nodes.values()],
            y=[n.y for n in self.nodes.values()],
            mode='markers',
            name='nodes',
            text=[str(n) for n in self.nodes.values()],
            hoverinfo='text',
            marker=dict(size=10, color='rgb(0,0,0)')
        )
        edges = [go.Scatter(
            x=[self.nodes[a].x, self.nodes[b].x],
            y=[self.nodes[a].y, self.nodes[b].y],
            mode='lines',
            name='({}, {})'.format(a, b)
        ) for (a, b) in self.edges]
        data = edges + [nodes]
        layout = go.Layout(showlegend=False,
                           hovermode='closest',
                           width=900,
                           height=900,
                           yaxis=dict(zeroline=False),
                           xaxis=dict(zeroline=False))
        self.graph = go.Figure(data=data, layout=layout)

    def save_graph(self, filename):
        if not filename.endswith('.html'):
            filename += '.html'
        py.plot(self.graph, filename=filename, auto_open=False)

    def render_graph(self, filename=None):
        pass

