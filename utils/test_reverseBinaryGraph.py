from unittest import TestCase
from utils.graph import ReverseBinaryGraph, Vertex

__author__ = 'msoum'


class TestReverseBinaryGraph(TestCase):
    def setUp(self):
        self.graph = ReverseBinaryGraph()

    def test_creation(self):
        self.assertEqual(0, len(self.graph.leaves))

    def test_one_leave(self):
        self.graph.add_leave(Vertex())
        self.assertEqual(1, len(self.graph.leaves))

    def test_two_leaves(self):
        self.graph.add_leave(Vertex())
        self.graph.add_leave(Vertex())
        self.assertEqual(2, len(self.graph.leaves))
        self.assertIsNotNone(self.graph.leaves[0].parent)
        self.assertIsNotNone(self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)

    def test_three_leaves(self):
        self.graph.add_leave(Vertex())
        self.graph.add_leave(Vertex())
        self.graph.add_leave(Vertex())
        self.assertEqual(3, len(self.graph.leaves))
        self.assertIsNotNone(self.graph.leaves[0].parent)
        self.assertIsNotNone(self.graph.leaves[1].parent)
        self.assertIsNotNone(self.graph.leaves[2].parent)
        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[0].parent.parent, self.graph.leaves[2].parent)

    def test_four_leaves(self):
        self.graph.add_leave(Vertex())
        self.graph.add_leave(Vertex())
        self.graph.add_leave(Vertex())
        self.graph.add_leave(Vertex())
        self.assertEqual(4, len(self.graph.leaves))
        self.assertIsNotNone(self.graph.leaves[0].parent)
        self.assertIsNotNone(self.graph.leaves[1].parent)
        self.assertIsNotNone(self.graph.leaves[2].parent)
        self.assertIsNotNone(self.graph.leaves[3].parent)
        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[2].parent, self.graph.leaves[3].parent)
        self.assertIs(self.graph.leaves[0].parent.parent, self.graph.leaves[2].parent.parent)
