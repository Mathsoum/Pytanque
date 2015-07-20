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

    def test_five_leaves(self):
        vertex_1 = Vertex()
        self.graph.add_leave(vertex_1)
        vertex_2 = Vertex()
        self.graph.add_leave(vertex_2)
        vertex_3 = Vertex()
        self.graph.add_leave(vertex_3)
        vertex_4 = Vertex()
        self.graph.add_leave(vertex_4)
        vertex_5 = Vertex()
        self.graph.add_leave(vertex_5)
        self.assertEqual(5, len(self.graph.leaves))
        self.assertIsNotNone(vertex_1.parent)
        self.assertIsNotNone(vertex_2.parent)
        self.assertIsNotNone(vertex_3.parent)
        self.assertIsNotNone(vertex_4.parent)
        self.assertIsNotNone(vertex_5.parent)
        self.assertIs(vertex_1.parent, vertex_2.parent)
        self.assertIs(vertex_3.parent, vertex_4.parent)
        self.assertIs(vertex_1.parent.parent, vertex_5.parent)
        self.assertIs(vertex_1.parent.parent.parent, vertex_5.parent.parent)
