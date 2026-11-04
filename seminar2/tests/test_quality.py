import json
import tempfile
import unittest
import urllib.request
from pathlib import Path

from seminar2 import mcp_server as srv
from seminar2.cities.graph import load_graph, load_roads
from seminar2.cities.quality import (
    QUALITY_FACTOR,
    best_quality_route,
    cost_adjacency,
    road_cost,
)
from seminar2.live import hub

HEADER = "city_a,city_b,km,quality\n"


def write(text):
    d = tempfile.TemporaryDirectory()
    p = Path(d.name) / "cities.csv"
    p.write_text(text, encoding="utf-8")
    return d, p


class LoaderTests(unittest.TestCase):
    def check_error(self, text, *fragments):
        d, p = write(text)
        with d, self.assertRaises(ValueError) as cm:
            load_roads(p)
        for f in (str(p), *fragments):
            self.assertIn(f, str(cm.exception))

    def test_real_data_is_symmetric(self):
        roads = load_roads()
        self.assertEqual(roads["Lezhë"]["Tirana"], "highway")
        self.assertEqual(roads["Tirana"]["Lezhë"], "highway")
        self.assertEqual(set(roads), set(load_graph()))

    def test_bad_quality_names_file_and_line(self):
        self.check_error(HEADER + "A,B,10,good\nB,C,5,bumpy\n", "line 3", "bumpy")

    def test_empty_quality_is_an_error(self):
        self.check_error(HEADER + "A,B,10,\n", "line 2")

    def test_missing_column_is_an_error_for_load_roads_only(self):
        d, p = write("city_a,city_b,km\nA,B,10\n")
        with d:
            self.assertEqual(load_graph(p), {"A": {"B": 10}, "B": {"A": 10}})
            with self.assertRaises(ValueError) as cm:
                load_roads(p)
            self.assertIn("quality", str(cm.exception))

    def test_load_graph_keeps_shape_with_quality_column(self):
        g = load_graph()
        self.assertEqual(g["Shkodër"], {"Lezhë": 40})
        self.assertIsInstance(g["Lezhë"]["Tirana"], int)


class CostModelTests(unittest.TestCase):
    def test_factors_rank_quality(self):
        f = QUALITY_FACTOR
        self.assertEqual(f, {"highway": 1.0, "good": 1.3, "fair": 1.8, "poor": 2.5})

    def test_road_cost(self):
        self.assertEqual(road_cost(100, "highway"), 100)
        self.assertEqual(road_cost(62, "good"), 80.6)
        self.assertEqual(road_cost(123, "poor"), 307.5)

    def test_better_road_can_beat_shorter_one(self):
        g = {"A": {"B": 60, "C": 50}, "B": {"A": 60, "C": 50}, "C": {"A": 50, "B": 50}}
        # direct A-B 60 km poor (150) vs A-C-B 100 km on highways (100)
        q = {"A": {"B": "poor", "C": "highway"}, "B": {"A": "poor", "C": "highway"},
             "C": {"A": "highway", "B": "highway"}}
        r = best_quality_route(g, q, "A", "B")
        self.assertEqual((r["route"], r["total_km"], r["quality_cost"], r["worst_road"]),
                         (["A", "C", "B"], 100, 100, "highway"))
        self.assertEqual(cost_adjacency(g, q)["A"]["B"], 150)

    def test_same_city_and_unreachable(self):
        g, q = {"A": {"B": 1}, "B": {"A": 1}}, {"A": {"B": "fair"}, "B": {"A": "fair"}}
        r = best_quality_route(g, q, "A", "A")
        self.assertEqual((r["route"], r["total_km"], r["legs"]), (["A"], 0, []))
        self.assertIsNone(best_quality_route(g, q, "A", "Z"))


class RealDataTests(unittest.TestCase):
    def setUp(self):
        hub.stop()

    tearDown = setUp

    def test_shkoder_korce(self):
        r = srv.best_quality_route("shkoder", "KORCE")
        self.assertEqual(list(r), ["from", "to", "route", "total_km", "quality_cost",
                                   "legs", "worst_road"])
        self.assertEqual(r["route"], ["Shkodër", "Lezhë", "Tirana", "Elbasan", "Korçë"])
        self.assertEqual((r["total_km"], r["worst_road"]), (267, "poor"))
        self.assertEqual(r["quality_cost"], 52 + 62 + 54.6 + 307.5)
        self.assertEqual(r["legs"][0], {"from": "Shkodër", "to": "Lezhë", "km": 40, "quality": "good"})

    def test_shkoder_vlore_differs_from_shortest(self):
        short = srv.shortest_route("Shkodër", "Vlorë")
        best = srv.best_quality_route("Shkodër", "Vlorë")
        self.assertEqual(short["route"], ["Shkodër", "Lezhë", "Durrës", "Fier", "Vlorë"])
        self.assertEqual(short["total_km"], 228)
        self.assertEqual(best["route"], ["Shkodër", "Lezhë", "Tirana", "Durrës", "Fier", "Vlorë"])
        self.assertEqual((best["total_km"], best["worst_road"]), (256, "good"))
        self.assertGreater(best["total_km"], short["total_km"])

    def test_bad_city(self):
        r = srv.best_quality_route("Narnia", "Tirana")
        self.assertIn("Narnia", r["error"])
        self.assertIn("Tirana", r["cities"])

    def test_publishes_to_viewer(self):
        url = hub.start(port=0)
        srv.best_quality_route("Shkodër", "Vlorë")
        with urllib.request.urlopen(url + "sessions/latest", timeout=5) as r:
            s = json.load(r)
        self.assertEqual((s["tool"], s["result"]["unit"]), ("best_quality_route", "cost"))


if __name__ == "__main__":
    unittest.main()
