"""Build the A* input graphs from the seminar 2 datasets.

`a_star_search` expects {node: [(neighbour, cost), ...]}. Seminar 2's loaders
return {city: {neighbour: km}} (cities) and {room: [neighbours]} (maze), so this
module only converts shapes; reading and validating the CSVs stays in seminar 2.
"""

# pairwise yields consecutive pairs: [a, b, c] -> (a, b), (b, c)
from itertools import pairwise

# load_graph reads and validates cities.csv into {city: {neighbour: km}};
# load_maze reads and validates the maze CSVs into a Maze record
from seminar2.cities.graph import load_graph
from seminar2.maze.maze import load_maze


def to_astar(adjacency):
    """Convert a seminar 2 adjacency dict to the A* list-of-tuples shape.

    Weighted {node: {neighbour: cost}} keeps its costs; unweighted
    {node: [neighbours]} gets cost 1 per edge (one door = one step).
    """
    graph = {}  # the converted graph we fill in and return
    for node, neighbours in adjacency.items():  # visit every node with its neighbours
        if isinstance(neighbours, dict):  # a dict means a weighted graph (cities: neighbour -> km)
            graph[node] = sorted(neighbours.items())  # (neighbour, km) pairs, sorted so the order is stable
        else:  # otherwise it is a plain list of neighbours (maze rooms, no weights)
            graph[node] = [(n, 1) for n in sorted(neighbours)]  # every door costs one step
    return graph  # {node: [(neighbour, cost), ...]}, ready for a_star_search


def city_graph(path=None):
    """Albanian cities graph, edge cost in km."""
    # use seminar 2's default cities.csv unless another CSV path is given, then convert it
    return to_astar(load_graph() if path is None else load_graph(path))


def maze_graph():
    """Maze graph (cost 1 per door) plus its entrance and exit rooms."""
    maze = load_maze()  # Maze record: rooms, entrance, exit, doors, adjacency
    return to_astar(maze.adjacency), maze.entrance, maze.exit  # graph plus where the search starts and ends


def path_cost(graph, path):
    """Total cost of a path in an A* graph."""
    # for each step a -> b, look up b's cost in a's neighbour list and add them all up
    return sum(dict(graph[a])[b] for a, b in pairwise(path))


if __name__ == "__main__":  # runs only with `python -m seminar3.graph`, not on import
    # the A* search from the starter code (imported here so importing this module stays light)
    from seminar3.seminar_3_initial_code import a_star_search

    cities = city_graph()  # build the cities graph from cities.csv
    for city, roads in cities.items():  # print each city with its roads
        print(f"{city}: {roads}")  # e.g. Shkodër: [('Lezhë', 40)]
    path = a_star_search(cities, "Shkodër", "Korçë")  # search from the north to the south-east
    print(f"\nShkodër -> Korçë: {' -> '.join(path)} ({path_cost(cities, path)} km)")  # route and its length

    maze, entrance, exit_room = maze_graph()  # build the maze graph and get its start and goal rooms
    path = a_star_search(maze, entrance, exit_room)  # search from the entrance to the exit
    print(f"Maze {entrance} -> {exit_room}: {path} ({path_cost(maze, path)} doors)")  # rooms passed and door count
