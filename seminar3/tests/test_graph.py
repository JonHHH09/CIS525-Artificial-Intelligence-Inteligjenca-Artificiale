# stdlib test framework used across the repo
import unittest

# load_graph: the original seminar 2 graph, used as the reference;
# seminar3.graph: the code under test;
# a_star_search: the A* search the graphs are built for
from seminar2.cities.graph import load_graph
from seminar3.graph import city_graph, maze_graph, path_cost, to_astar
from seminar3.seminar_3_initial_code import a_star_search


class ToAstarTest(unittest.TestCase):  # checks the shape conversion on its own, with tiny graphs
    def test_weighted_keeps_costs(self):
        # a weighted dict becomes sorted (neighbour, cost) tuples with the same costs
        self.assertEqual(to_astar({"A": {"C": 3, "B": 1}}), {"A": [("B", 1), ("C", 3)]})

    def test_unweighted_costs_one(self):
        # a plain neighbour list becomes sorted tuples where every edge costs 1
        self.assertEqual(to_astar({1: [6, 2]}), {1: [(2, 1), (6, 1)]})


class CityGraphTest(unittest.TestCase):  # checks the real cities dataset
    def test_same_edges_as_seminar2(self):
        source = load_graph()  # seminar 2 shape: {city: {neighbour: km}}
        graph = city_graph()  # seminar 3 shape: {city: [(neighbour, km), ...]}
        self.assertEqual(graph.keys(), source.keys())  # no city was lost or added
        for city, roads in graph.items():  # compare every city's roads
            self.assertEqual(dict(roads), source[city])  # same neighbours with the same km

    def test_astar_matches_dijkstra(self):
        graph = city_graph()  # build the cities graph
        path = a_star_search(graph, "Shkodër", "Korçë")  # run A* on the pinned seminar 2 route
        self.assertEqual((path[0], path[-1]), ("Shkodër", "Korçë"))  # path starts and ends where asked
        self.assertEqual(path_cost(graph, path), 267)  # same length Dijkstra found in seminar 2


class MazeGraphTest(unittest.TestCase):  # checks the real maze dataset
    def test_astar_matches_bfs(self):
        graph, entrance, exit_room = maze_graph()  # maze graph plus its start and goal rooms
        path = a_star_search(graph, entrance, exit_room)  # run A* from entrance to exit
        self.assertEqual(path_cost(graph, path), 12)  # same door count BFS found in seminar 2


if __name__ == "__main__":  # lets the file run directly as well as through discover
    unittest.main()  # run every test in this file
