from unittest import TestCase
from utils.graph import ReverseBinaryGraph

__author__ = 'msoum'


class TestReverseBinaryGraph(TestCase):
    def setUp(self):
        self.graph = ReverseBinaryGraph()

    def test_creation(self):
        self.assertEqual(0, len(self.graph.leaves))

    def test_one_leave(self):
        self.graph.add_leave(0)

        self.assertEqual(1, len(self.graph.leaves))
