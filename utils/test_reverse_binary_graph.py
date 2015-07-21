from unittest import TestCase

from utils.graph import ReverseBinaryGraph

__author__ = 'msoum'


class TestReverseBinaryGraph(TestCase):
    def test_creation(self):
        self.graph = ReverseBinaryGraph([])
        self.assertEqual(0, len(self.graph.leaves))

    def test_one_leave(self):
        self.graph = ReverseBinaryGraph([1])
        self.assertEqual(1, len(self.graph.leaves))

    def test_two_leaves(self):
        self.graph = ReverseBinaryGraph(range(1, 3))
        self.assertEqual(2, len(self.graph.leaves))
        for node in [it.parent for it in self.graph.leaves]:
            self.assertIsNotNone(node)

        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)

    def test_three_leaves(self):
        self.graph = ReverseBinaryGraph(range(1, 4))
        self.assertEqual(3, len(self.graph.leaves))
        for node in [it.parent for it in self.graph.leaves]:
            self.assertIsNotNone(node)

        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[0].parent.parent, self.graph.leaves[2].parent)

    def test_four_leaves(self):
        self.graph = ReverseBinaryGraph(range(1, 5))
        self.assertEqual(4, len(self.graph.leaves))
        for node in [it.parent for it in self.graph.leaves]:
            self.assertIsNotNone(node)

        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[2].parent, self.graph.leaves[3].parent)
        self.assertIs(self.graph.leaves[0].parent.parent, self.graph.leaves[2].parent.parent)

    def test_five_leaves(self):
        self.graph = ReverseBinaryGraph(range(1, 6))
        self.assertEqual(5, len(self.graph.leaves))
        for node in [it.parent for it in self.graph.leaves]:
            self.assertIsNotNone(node)

        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[0].parent.parent, self.graph.leaves[2].parent)
        self.assertIs(self.graph.leaves[3].parent, self.graph.leaves[4].parent)
        self.assertIs(self.graph.leaves[0].parent.parent.parent, self.graph.leaves[3].parent.parent)

    def test_seven_leaves(self):
        self.graph = ReverseBinaryGraph(range(1, 8))
        self.assertEqual(7, len(self.graph.leaves))
        for node in [it.parent for it in self.graph.leaves]:
            self.assertIsNotNone(node)

        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[2].parent, self.graph.leaves[3].parent)
        self.assertIs(self.graph.leaves[4].parent, self.graph.leaves[5].parent)
        self.assertIs(self.graph.leaves[4].parent.parent, self.graph.leaves[6].parent)
