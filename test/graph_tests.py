from utils.graph import ReverseBinaryGraph

__author__ = 'msoum'

import unittest


class GraphTestCase(unittest.TestCase):
    def setUp(self):
        self.graph = ReverseBinaryGraph()

    def testCreation(self):
        self.assertEqual(0, len(self.graph.leaves))
