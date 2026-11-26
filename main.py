"""CLI demo: python main.py [source] [destination]   |   python main.py --benchmark"""
import sys

from src.bellman_ford import bellman_ford
from src.dijkstra import dijkstra
from src.graph import build_sample_city
from src.utils import reconstruct_path


def main():
    if "--benchmark" in sys.argv:
        from src.benchmark import run
        return run()
    g = build_sample_city()
    src = sys.argv[1] if len(sys.argv) > 2 else "Airport"
    dst = sys.argv[2] if len(sys.argv) > 2 else "Old Town"
    if src not in g.vertices or dst not in g.vertices:
        sys.exit(f"Unknown location. Choose from: {', '.join(sorted(g.vertices))}")
    for name, fn in (("Dijkstra", dijkstra), ("Bellman-Ford", bellman_ford)):
        dist, prev = fn(g, src)
        print(f"[{name}] {src} -> {dst}: {' -> '.join(reconstruct_path(prev, src, dst))}  (cost {dist[dst]})")


if __name__ == "__main__":
    main()
