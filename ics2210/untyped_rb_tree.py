#!/usr/bin/env python3

from .untyped_tree import Direction, Node, Tree
from statistics import mean, median, variance
from enum import IntEnum
from random import randint, seed
from math import sqrt


class Color(IntEnum):
    RED = 0
    BLACK = 1


def is_black(node):
    return node is None or node.color == Color.BLACK


class RBNode(Node):
    def __init__(self, value: int):
        super().__init__(value)
        self.color = Color.BLACK

    def str_value(self):
        return f"{'R' if self.color == Color.RED else 'B'}{self.value}"

    def sibling_is_red(self):
        parent = self.parent  # assuming the parent exists

        return not is_black(parent.child[1 - parent.dir(self)])

    def get_sibling(self):
        parent = self.parent  # assuming the parent exists

        return parent.child[1 - parent.dir(self)]


class RBTree(Tree):
    num_of_rotations: list[int]

    def __init__(self, enable_stats: bool = False):
        super().__init__(enable_stats=enable_stats)

        if self.enable_stats:
            self.num_of_rotations = []

    def fix(self, node):
        current = node

        parent = current.parent

        if self.enable_stats:
            rotations = 0

        while not is_black(parent):
            grandparent = (
                parent.parent
            )  # parent is not None due to the is_black check and grandparent exists since parent is red

            if parent.sibling_is_red():
                sibling = (
                    parent.get_sibling()
                )  # sibling exists since it is red i.e. it is not None

                # invert the color
                sibling.color = Color.BLACK
                parent.color = Color.BLACK

                if grandparent.parent is not None:
                    grandparent.color = Color.RED
            else:
                direction = parent.dir(current)
                parent_direction = grandparent.dir(parent)

                if parent_direction == direction:
                    grandparent.rotate(Direction.from_int(1 - parent_direction))

                    grandparent.color = Color.RED
                    parent.color = Color.BLACK

                    if self.enable_stats:
                        rotations += 1

                        self.num_of_rotations.append(rotations)

                    return parent
                else:
                    parent.rotate(Direction.from_int(1 - direction))
                    grandparent.rotate(Direction.from_int(1 - parent_direction))

                    current.color = Color.BLACK
                    grandparent.color = Color.RED

                    if self.enable_stats:
                        rotations += 1

                        self.num_of_rotations.append(rotations)

                    return current

            current, parent = grandparent, grandparent.parent

        if self.enable_stats:
            self.num_of_rotations.append(rotations)

        return current

    def insert(self, node):
        if self.root is None:
            self.root = node
        else:
            node.color = Color.RED

            node = self.fix(super().insert(node))

            self.root = node if node.parent is None else self.root

    def insert_value(self, value):
        self.insert(RBNode(value))

    def compute_stats(self):
        if not self.enable_stats:
            return

        min_steps = min(self.num_of_steps)
        max_steps = max(self.num_of_steps)
        mean_steps = mean(self.num_of_steps)
        deviation_steps = sqrt(variance(self.num_of_steps))
        median_steps = median(self.num_of_steps)

        print(
            f"""Min Steps: {min_steps}
Max Steps: {max_steps}
Mean Steps: {mean_steps}
Standard Deviation Steps: {deviation_steps}
Median Step: {median_steps}"""
        )

        min_rotations = min(self.num_of_rotations)
        max_rotations = max(self.num_of_rotations)
        mean_rotations = mean(self.num_of_rotations)
        deviation_rotations = sqrt(variance(self.num_of_rotations))
        median_rotations = median(self.num_of_rotations)

        print(
            f"""Min Rotations: {min_rotations}
Max Rotations: {max_rotations}
Mean Rotations: {mean_rotations}
Standard Deviation Rotations: {deviation_rotations}
Median Rotations: {median_rotations}"""
        )

        print(f"Height: {self.calc_height()}")

        print(f"Leaves: {self.calc_leaves()}")


def example():
    tree = RBTree(enable_stats=True)

    seed(10)

    list_of_values = [randint(1, 50) for _ in range(20)]

    print(list_of_values)

    for value in list_of_values:
        tree.insert_value(value)

    tree.draw()
    tree.compute_stats()

    return tree
