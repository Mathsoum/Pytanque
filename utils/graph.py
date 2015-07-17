__author__ = 'msoum'


class Vertex:
    def __init__(self):
        self.parent = None
        self.left = None
        self.right = None

        self.data = None


class ReverseBinaryGraph:
    def __init__(self):
        self.leaves = []

    def add_leave(self, data):
        self.leaves.append(data)
