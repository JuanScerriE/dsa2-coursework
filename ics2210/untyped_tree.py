#!/usr/bin/env python3

from enum import IntEnum
from collections import deque


def get_addr(object) -> str:
    return "None" if object is None else str(id(object))


class Direction(IntEnum):
    LEFT = 0
    RIGHT = 1

    @staticmethod
    def from_int(value):
        return Direction.LEFT if value <= 0 else Direction.RIGHT


class Node:
    def __init__(self, value):
        self.value = value
        self.parent = None
        self.child = [None, None]

    def __str__(self) -> str:
        return f"""{get_addr(self)} {{
  .value = {self.value},
  .parent = {get_addr(self.parent)},
  .child = [{get_addr(self.child[Direction.LEFT])}, {get_addr(self.child[Direction.RIGHT])}],
}}"""

    def __repr__(self) -> str:
        return f"{get_addr(self)} {{.value = {self.value}}}"

    def left(self):
        return self.child[Direction.LEFT]

    def right(self):
        return self.child[Direction.RIGHT]

    def is_leaf(self):
        return self.left() is None and self.right() is None

    def value_dir(self, other):
        return Direction.LEFT if self.value > other.value else Direction.RIGHT

    def dir(self, other):
        return Direction.LEFT if self.left() is other else Direction.RIGHT

    def can_step(self, direction):
        return self.child[direction] is not None

    def rotate(self, direction):
        child = self.child[1 - direction]

        if child is None:
            return self

        if self.parent is None:
            child.parent = None
        else:
            child.parent = self.parent

            self.parent.child[self.parent.dir(self)] = child

        self.child[1 - direction] = child.child[direction]

        if self.child[1 - direction] is not None:
            self.child[1 - direction].parent = self

        child.child[direction] = self

        self.parent = child

        return child

    def str_value(self) -> str:
        return str(self.value)


class Tree:
    def __init__(self, enable_stats: bool = False):
        self.root = None
        self.height = 0
        self.leaves = 0
        self.enable_stats = enable_stats

        if enable_stats:
            self.num_of_steps = []

    def insert(self, node):
        current = self.root

        if current is None:
            return node

        if self.enable_stats:
            steps = 0

        insert_direction = current.value_dir(node)

        while current.can_step(insert_direction):
            current = current.child[insert_direction]

            insert_direction = current.value_dir(node)

            if self.enable_stats:
                steps += 1

        node.parent = current

        current.child[insert_direction] = node

        if self.enable_stats:
            self.num_of_steps.append(steps)

        return node

    def insert_value(self, value):
        raise NotImplementedError

    def calc_height(self):
        def _calc_height(node) -> int:
            if node is None:
                return 0

            return (
                max(
                    _calc_height(node.left()),
                    _calc_height(node.right()),
                )
                + 1
            )

        return _calc_height(self.root) - 1

    def calc_leaves(self) -> int:
        def _calc_leaves(node) -> int:
            if node is None:
                return 0

            if node.is_leaf():
                return 1
            else:
                return _calc_leaves(node.left()) + _calc_leaves(node.right())

        return _calc_leaves(self.root)

    def draw(self):
        if self.root is None:
            print("{}")
        else:
            height = self.calc_height()

            def calc_indent(height: int) -> int:
                return ((2 ** (height + 1)) - 1) // 2

            indent = calc_indent(height)

            final_queue = deque()

            queue = deque([(0, indent, height, self.root)])

            cell_width: int = 0

            while queue:
                (level, indent, height, node) = queue.popleft()

                cell_width = max(cell_width, len(node.str_value()))

                final_queue.append((level, indent, node))

                step = calc_indent(height - 1) + 1

                if (left := node.child[Direction.LEFT]) is not None:
                    queue.append((level + 1, indent - step, height - 1, left))

                if (right := node.child[Direction.RIGHT]) is not None:
                    queue.append((level + 1, indent + step, height - 1, right))

            if cell_width % 2 == 0:
                cell_width += 1

            cell_width += 2

            decoration = list(" " * cell_width)

            decoration[cell_width // 2] = "^"

            decoration = "".join(decoration)

            prev_indent, prev_level = 0, 0

            pretty_repeat = deque()

            while final_queue:
                (level, indent, node) = final_queue.popleft()

                if level > prev_level:
                    # do some pretty printing

                    print("\n", end="")

                    prev_indent = 0

                    while pretty_repeat:
                        pretty_indent = pretty_repeat.popleft()

                        print(
                            f"{(' ' * cell_width) * (pretty_indent - prev_indent)}{decoration}",
                            end="",
                        )

                        prev_indent = pretty_indent + 1

                    print("\n", end="")

                    prev_level, prev_indent = level, 0

                pretty_repeat.append(indent)

                print(
                    f"{(' ' * cell_width) * (indent - prev_indent)}[{node.str_value(): <{cell_width - 2}}]",
                    end="",
                )

                prev_indent = indent + 1

        print()
