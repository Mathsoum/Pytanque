__author__ = 'msoum'


class Vertex:
    def __init__(self, data=None):
        self.parent = None
        self.left = None
        self.right = None
        self.data = data

    def __str__(self):
        return str(self.data)

    def __hash__(self):
        return hash(self.parent) + hash(self.left) + hash(self.right) + hash(self.data)

    def __eq__(self, other):
        return other.parent is self.parent and other.left is self.left and other.right is self.right and other.data == self.data


class ReverseBinaryGraph:
    def __init__(self, leaves_list):
        self.leaves = [Vertex(it) for it in leaves_list]
        self.build_tree(leaves_list)

    def build_tree(self, leaves_list):
        if len(leaves_list) == 0:
            return Vertex()
        if len(leaves_list) == 1:
            leave = Vertex(leaves_list[0])
            data_list = [it.data for it in self.leaves]
            idx = data_list.index(leaves_list[0])
            self.leaves[idx] = leave
            return leave
        else:  # TODO Sub-trees construction could be computed in parallel
            left_list, right_list = self.split_leave_list(leaves_list)
            left_root = self.build_tree(left_list)
            right_root = self.build_tree(right_list)
            return self.create_parent(left_root, right_root)

    def split_leave_list(self, leaves_list):
        power, rest = self.power_two_decomposition(len(leaves_list))
        if rest <= power // 2:
            left_list = leaves_list[:(power // 2) + rest]
            right_list = leaves_list[(power // 2) + rest:]
        else:
            left_list = leaves_list[:power]
            right_list = leaves_list[power:]

        return left_list, right_list

    @staticmethod
    def create_parent(left_root, right_root):
        parent = Vertex()
        parent.left = left_root
        parent.right = right_root
        left_root.parent = right_root.parent = parent
        return parent

    @staticmethod
    def power_two_decomposition(number):
        if number == 1:
            return 0, 1
        else:
            power = 2
            previous = 2
            while power <= number:
                previous = power
                power *= 2

            return previous, number - previous

    def level_count(self):
        level_count = 1
        leave = self.leaves[0]
        while leave.parent is not None:
            level_count += 1
            leave = leave.parent

        return level_count

    def get_node_list_for_level(self, level):
        if level == 0:
            return self.leaves
        else:
            return set([it.parent for it in self.get_node_list_for_level(level - 1)])

    def get_sibling(self, vertex):
        return self.__get_sibling(vertex, self.leaves)

    def __get_sibling(self, vertex, leaves):
        if vertex.parent is None:
            return None

        if vertex not in leaves:
            parents = []
            for item in leaves:
                if item.parent not in parents:
                    parents.append(item.parent)
            sibling = self.__get_sibling(vertex, parents)
            return sibling
        else:
            for item in leaves:
                if item is vertex:
                    if item.parent.left is item:
                        return item.parent.right
                    elif item.parent.right is item:
                        return item.parent.left
