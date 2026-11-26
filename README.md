# Smart City Route Optimization System

Finds the shortest route between locations in a city. Locations are **vertices**, roads are **weighted edges**.
Implements **Dijkstra's** and **Bellman-Ford** and compares their performance across graph sizes.

## Project structure
```
main.py                 CLI demo + benchmark entry point
src/graph.py            Graph class, sample city, random city generator
src/dijkstra.py         Dijkstra (min-heap)
src/bellman_ford.py     Bellman-Ford (early exit + negative-cycle detection)
src/utils.py            Path reconstruction
src/benchmark.py        Runtime comparison -> results/
tests/                  pytest suite
results/                benchmark.csv, benchmark.png
```

## Run
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py                       # Airport -> Old Town on the sample city
python main.py "Market" "Stadium"    # any two locations
python main.py --benchmark           # compare algorithms on 50..1600 locations
python -m pytest -q                  # run tests
```

## Complexity
| Algorithm | Time | Space | Negative weights |
|---|---|---|---|
| Dijkstra (binary heap) | O((V + E) log V) | O(V) | No |
| Bellman-Ford | O(V · E) | O(V) | Yes (detects negative cycles) |

## Benchmark (random connected city, avg degree ~12, best of 3 runs)
| V | E (directed) | Dijkstra (ms) | Bellman-Ford (ms) |
|---|---|---|---|
| 50 | 294 | 0.038 | 0.112 |
| 100 | 592 | 0.079 | 0.277 |
| 200 | 1194 | 0.164 | 0.591 |
| 400 | 2396 | 0.379 | 1.546 |
| 800 | 4798 | 0.898 | 3.514 |
| 1600 | 9594 | 2.073 | 9.180 |

Both algorithms return identical distances on every graph. See `results/benchmark.png`.

## Conclusion
- Dijkstra is 3-4x faster here and the gap widens as the graph grows, so it is the right choice for road networks (weights are never negative).
- Bellman-Ford is slower but supports negative weights and detects negative cycles, so use it when such weights are possible.
- Bellman-Ford's early exit keeps it fast on sparse city graphs where paths are short; its worst case is still O(V · E).
