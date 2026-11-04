"""Seminar 3: draw the cities graph from seminar_3_initial_code.py.

Writes seminar3/images/starter_graph.png with the A* path highlighted.
"""

from collections import deque
from itertools import pairwise
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # draw to files only, no window needed
import matplotlib.pyplot as plt

from seminar3.graph import path_cost
from seminar3.seminar_3_initial_code import GOAL, START, a_star_search, graph_data

IMAGES = Path(__file__).resolve().parent / "images"  # seminar3/images/

NODE = "#8fbce6"  # nodes off the path
PATH_NODE = "#d81b60"  # nodes on the A* path
EDGE = "#555555"  # edges off the path
LABEL = "#b00020"  # cost labels

# Node positions copied from the State Space slide (pixels / 100, y flipped so up is up)
CITY_POS = {
    "LE": (5.6, -2.4), "SH": (7.9, -3.3), "TR": (3.8, -3.5), "EL": (5.4, -4.1),
    "DR": (2.4, -4.5), "LU": (3.1, -6.0), "PR": (7.2, -5.5), "TP": (6.3, -6.5),
    "GJ": (8.8, -6.6), "SR": (10.3, -7.7), "FR": (3.9, -8.0), "VL": (6.4, -8.4),
}


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
                    "color": color, "lw": width, "shrinkA": 18, "shrinkB": 18, "mutation_scale": 20,
                },
                zorder=1,
            )
            ax.text(
                (x1 + x2) / 2, (y1 + y2) / 2, f"{cost}{unit}",
                ha="center", va="center", fontsize=10, color=LABEL,
                bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": "none"}, zorder=3,
            )

    for node, (x, y) in pos.items():  # nodes on top of the edges
        ax.scatter(x, y, s=1300, zorder=2, clip_on=False, color=PATH_NODE if node in path else NODE, edgecolor="black")
        ax.text(x, y, str(node), ha="center", va="center", fontsize=9, fontweight="bold",
                color="white" if node in path else "black", zorder=4)

    ax.set_title(title, pad=20)
    ax.set_aspect("equal")
    ax.margins(0.08)
    ax.axis("off")
    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)  # create seminar3/images/ if missing
    fig.savefig(out, dpi=200)
    plt.close(fig)


def main():
    path = a_star_search(graph_data, START, GOAL)  # same search the starter's __main__ runs
    out = IMAGES / "starter_graph.png"
    draw(graph_data, CITY_POS, path,
         f"Cities graph: A* path {START} -> {GOAL} = {' -> '.join(path)} (cost {path_cost(graph_data, path)})", out)
    print(f"saved {out}")


if __name__ == "__main__":
    main()
