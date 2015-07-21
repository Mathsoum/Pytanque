__author__ = 'msoum'


class Vertex:
    def __init__(self, data=None):
        self.parent = None
        self.left = None
        self.right = None
        self.data = data


class ReverseBinaryGraph:
    def __init__(self):
        self.leaves = []

    def add_leave(self, data):
        self.leaves.append(Vertex(data))
        if len(self.leaves) == 2:
            left = self.leaves[0]
            right = self.leaves[1]
            self.set_parent(left, right)
        elif len(self.leaves) == 3:
            left = self.leaves[0].parent
            right = self.leaves[2]
            self.set_parent(left, right)
        elif len(self.leaves) == 4:
            left = self.leaves[2]
            right = self.leaves[3]
            self.set_parent(left, right)
            left = self.leaves[0].parent
            right = self.leaves[2].parent
            self.set_parent(left, right, self.leaves[0].parent.parent)
        elif len(self.leaves) == 5:
            left = self.leaves[0].parent
            right = self.leaves[4]
            self.set_parent(left, right)
            left = self.leaves[4].parent
            right = self.leaves[2].parent
            self.set_parent(left, right, self.leaves[2].parent.parent)

    @staticmethod
    def set_parent(left, right, parent=Vertex()):
        left.parent = parent
        right.parent = parent
        parent.left = left
        parent.right = right
