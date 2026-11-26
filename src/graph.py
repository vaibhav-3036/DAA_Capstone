"""Weighted graph: locations are vertices, roads are weighted edges."""
import random
from collections import defaultdict


class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.adj = defaultdict(list)  # u -> [(v, weight)]
        self.vertices = set()

    def add_vertex(self, v):
        self.vertices.add(v)

    def add_edge(self, u, v, w):
        self.vertices.update((u, v))
        self.adj[u].append((v, w))
        if not self.directed:
            self.adj[v].append((u, w))

    def edges(self):
        """Yield every directed edge (u, v, w). Undirected roads yield both ways."""
        for u in self.vertices:
            for v, w in self.adj[u]:
                yield u, v, w

    def num_vertices(self):
        return len(self.vertices)

    def num_edges(self):
        return sum(len(n) for n in self.adj.values())


def build_sample_city():
    """Small named city used by the demo."""
    g = Graph()
    roads = [
        ("Airport", "Central Station", 12), ("Airport", "Tech Park", 9),
        ("Central Station", "Market", 4), ("Central Station", "University", 7),
        ("Tech Park", "University", 5), ("Tech Park", "Stadium", 11),
        ("Market", "Hospital", 6), ("University", "Hospital", 3),
        ("University", "Stadium", 8), ("Hospital", "Old Town", 5),
        ("Stadium", "Old Town", 4), ("Market", "Old Town", 14),
    ]
    for u, v, w in roads:
        g.add_edge(u, v, w)
    return g


def generate_random_city(n, extra_edges_factor=2, max_weight=100, seed=None):
    """Connected random graph: a random spanning tree plus extra roads."""
    rng = random.Random(seed)
    g = Graph()
    nodes = list(range(n))
    rng.shuffle(nodes)
    for i in range(1, n):  # spanning tree guarantees connectivity
        g.add_edge(nodes[i], nodes[rng.randrange(i)], rng.randint(1, max_weight))
    for _ in range(n * extra_edges_factor):
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v:
            g.add_edge(u, v, rng.randint(1, max_weight))
    return g
