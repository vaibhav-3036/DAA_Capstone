import pytest

from src.bellman_ford import NegativeCycleError, bellman_ford
from src.dijkstra import INF, dijkstra
from src.graph import Graph, build_sample_city, generate_random_city
from src.utils import reconstruct_path


def test_sample_city_known_answer():
    g = build_sample_city()
    for fn in (dijkstra, bellman_ford):
        dist, prev = fn(g, "Airport")
        assert dist["Old Town"] == 22
        assert reconstruct_path(prev, "Airport", "Old Town")[0] == "Airport"


def test_algorithms_agree_on_random_graphs():
    for seed in range(10):
        g = generate_random_city(60, seed=seed)
        assert dijkstra(g, 0)[0] == bellman_ford(g, 0)[0]


def test_unreachable_vertex():
    g = Graph()
    g.add_edge("A", "B", 1)
    g.add_vertex("C")
    for fn in (dijkstra, bellman_ford):
        dist, prev = fn(g, "A")
        assert dist["C"] == INF
        assert reconstruct_path(prev, "A", "C") == []


def test_bellman_ford_negative_edge_directed():
    g = Graph(directed=True)
    g.add_edge("A", "B", 4); g.add_edge("A", "C", 5); g.add_edge("C", "B", -3)
    assert bellman_ford(g, "A")[0]["B"] == 2


def test_bellman_ford_detects_negative_cycle():
    g = Graph(directed=True)
    g.add_edge("A", "B", 1); g.add_edge("B", "C", -2); g.add_edge("C", "A", -1)
    with pytest.raises(NegativeCycleError):
        bellman_ford(g, "A")


def test_dijkstra_rejects_negative_weight():
    g = Graph(directed=True)
    g.add_edge("A", "B", -1)
    with pytest.raises(ValueError):
        dijkstra(g, "A")
