"""Compare Dijkstra and Bellman-Ford across graph sizes. Writes results/benchmark.csv (+ png if matplotlib exists)."""
import csv
import os
import time

from .bellman_ford import bellman_ford
from .dijkstra import dijkstra
from .graph import generate_random_city

SIZES = [50, 100, 200, 400, 800, 1600]
RUNS = 3
OUT = os.path.join(os.path.dirname(__file__), "..", "results")


def timed(fn, g, src):
    best = float("inf")
    for _ in range(RUNS):
        t = time.perf_counter()
        res = fn(g, src)
        best = min(best, time.perf_counter() - t)
    return best, res


def run():
    os.makedirs(OUT, exist_ok=True)
    rows = []
    print(f"{'V':>6} {'E':>7} {'Dijkstra (ms)':>14} {'Bellman-Ford (ms)':>18} {'Speedup':>9} {'Match':>6}")
    for n in SIZES:
        g = generate_random_city(n, seed=n)
        src = next(iter(g.vertices))
        td, (dd, _) = timed(dijkstra, g, src)
        tb, (db, _) = timed(bellman_ford, g, src)
        rows.append([n, g.num_edges(), round(td * 1000, 3), round(tb * 1000, 3), dd == db])
        print(f"{n:>6} {g.num_edges():>7} {td*1000:>14.3f} {tb*1000:>18.3f} {tb/td:>8.1f}x {str(dd == db):>6}")
    with open(os.path.join(OUT, "benchmark.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["vertices", "directed_edges", "dijkstra_ms", "bellman_ford_ms", "results_match"])
        w.writerows(rows)
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        plt.figure(figsize=(7, 4.5))
        plt.plot([r[0] for r in rows], [r[2] for r in rows], "o-", label="Dijkstra")
        plt.plot([r[0] for r in rows], [r[3] for r in rows], "s-", label="Bellman-Ford")
        plt.xlabel("Number of locations (V)"); plt.ylabel("Time (ms)")
        plt.title("Shortest-path runtime vs graph size"); plt.legend(); plt.grid(alpha=.3)
        plt.tight_layout(); plt.savefig(os.path.join(OUT, "benchmark.png"), dpi=150)
        print("Saved results/benchmark.png")
    except ImportError:
        print("matplotlib not installed - skipped chart (pip install matplotlib)")


if __name__ == "__main__":
    run()
