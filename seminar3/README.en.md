# Seminar 3: A* search

[Shqip](README.md) · English · [Course index](../README.en.md)

**Status: in progress.**

## Contents

| File | Description |
|---|---|
| [`seminar_3_initial_code.py`](seminar_3_initial_code.py) | Provided starter code: `Node`, `a_star_search` and the example graph `graph_data` (A–G) |
| [`draw.py`](draw.py) | Draws `graph_data` with the A* path highlighted |
| [`graph.py`](graph.py) | Converts the Seminar 2 graphs (cities, maze) to the shape `a_star_search` expects |
| [`tests/`](tests/) | Tests for `graph.py`: same edges as Seminar 2, same results as Dijkstra and BFS |
| [`images/`](images/) | Generated figures |

## The graph

`graph_data` is directed and weighted: each node maps to a list of `(neighbour, cost)` pairs.

```python
graph_data = {
    'A': [('B', 1), ('C', 3)],
    'B': [('D', 2), ('E', 5)],
    'C': [('F', 4)],
    'D': [('G', 1)],
    'E': [('G', 2)],
    'F': [],
    'G': []
}
```

![Starter graph with the A* path](images/starter_graph.png)

Nodes are placed in columns by their distance in edges from A. The A* path is in pink.

## How A* works

Each `Node` keeps three values:

| Value | Meaning |
|---|---|
| `g` | cost of the path from the start to this node |
| `h` | estimated cost from this node to the goal (heuristic) |
| `f` | `g + h`: estimated cost of the full path through this node |

`a_star_search(graph, start, end)`:

1. Put the start node in the **open list** (a heap ordered by `f`).
2. Take the node with the lowest `f` and add it to the **closed list** (already expanded).
3. If it is the goal, follow the `parent` links back to the start and return the reversed path.
4. Otherwise, for each neighbour not in the closed list, compute `g`, `h` and `f` and push it onto the open list, unless it is already there with an equal or lower `f`.
5. Repeat until the open list is empty; then there is no path (`None`).

Result on `graph_data`: **A → B → D → G, cost 4** (1 + 2 + 1). The alternative A → B → E → G costs 8.

In the starter code `h = 0`, so `f = g` and the search behaves like Dijkstra: correct, but not guided toward the goal. A real heuristic must never overestimate the remaining cost (admissible), or A* can return a longer path.

## Running it

From the repo root:

```
uv run python seminar3/seminar_3_initial_code.py           # prints the path from A to G
uv run python -m seminar3.draw                             # writes images/starter_graph.png
uv run python -m seminar3.graph                            # A* on the Seminar 2 cities and maze graphs
uv run python -m unittest discover -s seminar3/tests -t .  # tests
```
