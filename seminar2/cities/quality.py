"""Road-quality cost model for the cities graph (U1).

A road costs km * QUALITY_FACTOR[quality], so a 100 km highway (100) beats a
60 km poor road (150). The cost adjacency feeds the normal Graph/Dijkstra.
"""

from seminar2.cities.graph import QUALITIES
from seminar2.graph_search import Graph

QUALITY_FACTOR = {"highway": 1.0, "good": 1.3, "fair": 1.8, "poor": 2.5}


def road_cost(km, quality):
    """Cost of one road; rounded so float noise (62 * 1.3) stays out of the output."""
    return round(km * QUALITY_FACTOR[quality], 1)


def cost_adjacency(graph, roads):
    """{city: {neighbour: cost}} from the km graph and the quality map."""
    return {a: {b: road_cost(km, roads[a][b]) for b, km in nbs.items()}
            for a, nbs in graph.items()}


def best_quality_route(graph, roads, start, goal):
    """Cheapest route by quality-weighted cost.

    Returns {"route", "total_km", "quality_cost", "legs", "worst_road"} or None
    if there is no route. legs is [{from, to, km, quality}]; worst_road is the
    worst quality on the route ("highway" for a zero-length route).
    """
    path, cost = Graph(cost_adjacency(graph, roads), weighted=True).shortest_path(start, goal)
    if path is None:
        return None
    legs = [{"from": a, "to": b, "km": graph[a][b], "quality": roads[a][b]}
            for a, b in zip(path, path[1:], strict=False)]
    worst = max((leg["quality"] for leg in legs), key=QUALITIES.index, default=QUALITIES[0])
    return {"route": path, "total_km": sum(leg["km"] for leg in legs),
            "quality_cost": round(cost, 1), "legs": legs, "worst_road": worst}
