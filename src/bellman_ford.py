"""Bellman-Ford algorithm. O(V * E). Handles negative weights, detects negative cycles."""
INF = float("inf")


class NegativeCycleError(Exception):
    pass


def bellman_ford(graph, source):
    dist = {v: INF for v in graph.vertices}
    prev = {v: None for v in graph.vertices}
    dist[source] = 0
    edges = list(graph.edges())
    for _ in range(len(graph.vertices) - 1):
        changed = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                prev[v] = u
                changed = True
        if not changed:  # early exit
            break
    for u, v, w in edges:  # V-th pass: any relaxation means a negative cycle
        if dist[u] != INF and dist[u] + w < dist[v]:
            raise NegativeCycleError("Graph contains a negative-weight cycle")
    return dist, prev
