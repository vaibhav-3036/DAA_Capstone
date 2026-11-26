"""Dijkstra's algorithm (binary heap). O((V + E) log V). Non-negative weights only."""
import heapq

INF = float("inf")


def dijkstra(graph, source):
    dist = {v: INF for v in graph.vertices}
    prev = {v: None for v in graph.vertices}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue  # stale entry
        for v, w in graph.adj[u]:
            if w < 0:
                raise ValueError("Dijkstra requires non-negative edge weights")
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev
