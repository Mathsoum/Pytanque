from unittest import TestCase

from domain.data_structures import Team
from utils.graph import ReverseBinaryGraph

__author__ = 'msoum'


class TestReverseBinaryGraph(TestCase):
    def setUp(self):
        self.graph = ReverseBinaryGraph()

    def test_creation(self):
        self.assertEqual(0, len(self.graph.leaves))

    def test_one_leave(self):
        self.graph.add_leave(Team('A', 'A'))
        self.assertEqual(1, len(self.graph.leaves))

    def test_two_leaves(self):
        self.graph.add_leave(Team('A', 'A'))
        self.graph.add_leave(Team('B', 'B'))
        self.assertEqual(2, len(self.graph.leaves))
        self.assertIsNotNone(self.graph.leaves[0].parent)
        self.assertIsNotNone(self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)

    def test_three_leaves(self):
        self.graph.add_leave(Team('A', 'A'))
        self.graph.add_leave(Team('B', 'B'))
        self.graph.add_leave(Team('C', 'C'))
        self.assertEqual(3, len(self.graph.leaves))
        self.assertIsNotNone(self.graph.leaves[0].parent)
        self.assertIsNotNone(self.graph.leaves[1].parent)
        self.assertIsNotNone(self.graph.leaves[2].parent)
        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[0].parent.parent, self.graph.leaves[2].parent)

    def test_four_leaves(self):
        self.graph.add_leave(Team('A', 'A'))
        self.graph.add_leave(Team('B', 'B'))
        self.graph.add_leave(Team('C', 'C'))
        self.graph.add_leave(Team('D', 'D'))
        self.assertEqual(4, len(self.graph.leaves))
        self.assertIsNotNone(self.graph.leaves[0].parent)
        self.assertIsNotNone(self.graph.leaves[1].parent)
        self.assertIsNotNone(self.graph.leaves[2].parent)
        self.assertIsNotNone(self.graph.leaves[3].parent)
        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[2].parent, self.graph.leaves[3].parent)
        self.assertIs(self.graph.leaves[0].parent.parent, self.graph.leaves[2].parent.parent)

    def test_five_leaves(self):
        self.graph.add_leave(Team('A', 'A'))
        self.graph.add_leave(Team('B', 'B'))
        self.graph.add_leave(Team('C', 'C'))
        self.graph.add_leave(Team('D', 'D'))
        self.graph.add_leave(Team('E', 'E'))
        self.assertEqual(5, len(self.graph.leaves))
        self.assertIsNotNone(self.graph.leaves[0].parent)
        self.assertIsNotNone(self.graph.leaves[1].parent)
        self.assertIsNotNone(self.graph.leaves[2].parent)
        self.assertIsNotNone(self.graph.leaves[3].parent)
        self.assertIsNotNone(self.graph.leaves[4].parent)
        self.assertIs(self.graph.leaves[0].parent, self.graph.leaves[1].parent)
        self.assertIs(self.graph.leaves[2].parent, self.graph.leaves[3].parent)
        self.assertIs(self.graph.leaves[0].parent.parent, self.graph.leaves[4].parent)
        self.assertIs(self.graph.leaves[0].parent.parent.parent, self.graph.leaves[4].parent.parent)
