# ./tests/test_edges.py
from json2sql.edges import create_graph_from_edges
import unittest


class TestEdges(unittest.TestCase):
    # A -> B -> C -> D -> E
    def test_linear_graph(self):
        edges = [
            {"from": "A", "to": "B"},
            {"from": "B", "to": "C"},
            {"from": "C", "to": "D"},
            {"from": "D", "to": "E"},
        ]

        nodes = create_graph_from_edges(edges)
        print(nodes)
        self.assertEqual(
            nodes, {0: "A", "A": "B", "B": "C", "C": "D", "D": "E", "E": ""}
        )

    # A -> B -> C -> D ... E -> F
    def test_two_graphs(self):
        edges = [
            {"from": "A", "to": "B"},
            {"from": "B", "to": "C"},
            {"from": "C", "to": "D"},
            {"from": "E", "to": "F"},
        ]

        nodes = create_graph_from_edges(edges)
        self.assertEqual(nodes, {0: "A", "A": "B", "B": "C", "C": "D", "D": ""})
        print(nodes)

    # A -> B -> C ... A -> D
    def test_branching_graph(self):
        edges = [
            {"from": "A", "to": "B"},
            {"from": "B", "to": "C"},
            {"from": "A", "to": "D"},
        ]

        nodes = create_graph_from_edges(edges)
        print(nodes)
        self.assertEqual(nodes, {0: "A", "A": "B", "B": "C", "C": ""})

    # A -> B -> C -> A
    def test_circular_graph(self):
        edges = [
            {"from": "A", "to": "B"},
            {"from": "B", "to": "C"},
            {"from": "C", "to": "A"},
        ]

        nodes = create_graph_from_edges(edges)
        print(nodes)
        self.assertEqual(nodes, {0: "A", "A": "B", "B": "C", "C": ""})
