"""Seminar 3: draw the A-G example graph from seminar_3_initial_code.py.

Writes seminar3/images/starter_graph.png with the A* path highlighted.
"""

from collections import deque
from itertools import pairwise
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # draw to files only, no window needed
import matplotlib.pyplot as plt

from seminar3.graph import path_cost
from seminar3.seminar_3_initial_code import a_star_search, graph_data

IMAGES = Path(__file__).resolve().parent / "images"  # seminar3/images/

NODE = "#8fbce6"  # nodes off the path
PATH_NODE = "#d81b60"  # nodes on the A* path
EDGE = "#555555"  # edges off the path
LABEL = "#b00020"  # cost labels


def layered_positions(graph, start):
    """Place nodes in columns by their BFS depth from `start` (for graphs with no coordinates)."""
    depth = {start: 0}  # how many edges each node is from the start
    queue = deque([start])  # BFS queue
    while queue:  # visit nodes level by level
        node = queue.popleft()  # next node to expand
        for neighbour, _ in graph.get(node, []):  # look at each outgoing edge
            if neighbour not in depth:  # first time we reach this node: its depth is final
                depth[neighbour] = depth[node] + 1
                queue.append(neighbour)
    for node in graph:  # nodes the start can't reach go in an extra last column
        depth.setdefault(node, max(depth.values()) + 1)

    columns = {}  # depth -> nodes in that column
    for node in sorted(depth):  # sorted so the drawing is the same on every run
        columns.setdefault(depth[node], []).append(node)
    pos = {}
    for d, nodes in columns.items():  # spread each column vertically around y = 0
        for i, node in enumerate(nodes):
            pos[node] = (d * 2.0, (len(nodes) - 1) / 2 - i)
    return pos


def draw(graph, pos, path, title, out, unit=""):
    """Draw `graph` at `pos`, highlight `path`, save the image to `out`."""
    fig, ax = plt.subplots(figsize=(10, 7))
    on_path = set(pairwise(path or []))  # edges the path uses, as (from, to) pairs

    drawn = set()  # undirected edges already drawn, so each is drawn once
    for a, edges in graph.items():
        for b, cost in edges:
            undirected = (a, cost) in graph.get(b, [])  # b also links back to a with the same cost
            if undirected and (b, a) in drawn:  # the reverse direction was already drawn
                continue
            drawn.add((a, b))
            used = (a, b) in on_path or (undirected and (b, a) in on_path)  # is this edge on the A* path?
            color, width = (PATH_NODE, 4) if used else (EDGE, 2)
            (x1, y1), (x2, y2) = pos[a], pos[b]
            ax.annotate(
                "", xy=(x2, y2), xytext=(x1, y1),
                arrowprops={
                    "arrowstyle": "-" if undirected else "-|>",  # arrow only for one-way edges
                    "color": color, "lw": width, "shrinkA": 22, "shrinkB": 22, "mutation_scale": 20,
                },
                zorder=1,
            )
            ax.text(
                (x1 + x2) / 2, (y1 + y2) / 2, f"{cost}{unit}",
                ha="center", va="center", fontsize=10, color=LABEL,
                bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none"}, zorder=3,
            )

    for node, (x, y) in pos.items():  # nodes on top of the edges
        ax.scatter(x, y, s=2000, zorder=2, color=PATH_NODE if node in path else NODE, edgecolor="black")
        ax.text(x, y, str(node), ha="center", va="center", fontsize=9, fontweight="bold",
                color="white" if node in path else "black", zorder=4)

    ax.set_title(title)
    ax.set_aspect("equal")
    ax.margins(0.12)
    ax.axis("off")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)  # create seminar3/images/ if missing
    fig.savefig(out, dpi=200)
    plt.close(fig)


def main():
    path = a_star_search(graph_data, "A", "G")  # same search the starter's __main__ runs
    out = IMAGES / "starter_graph.png"
    draw(graph_data, layered_positions(graph_data, "A"), path,
         f"Starter graph: A* path A -> G = {' -> '.join(path)} (cost {path_cost(graph_data, path)})", out)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
