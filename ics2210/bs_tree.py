from __future__ import annotations

from enum import IntEnum
from collections import deque
from typing import cast, Self, Any, Deque


def get_addr(object: Any) -> str:
    return "None" if object is None else str(id(object))


class Branch(IntEnum):
    LEFT = 0
    ROOT = 1
    RIGHT = 2


class Direction(IntEnum):
    LEFT = 0
    RIGHT = 1


class Node(object):
    value: int
    parent: Self | None
    child: list[Self | None]

    def __init__(self: Self, value: int):
        self.value = value
        self.parent = None
        self.child = [None, None]

    def __str__(self: Self) -> str:
        return f"""{get_addr(self)} {{
  .value = {self.value},
  .parent = {get_addr(self.parent)},
  .child = [{get_addr(self.child[Direction.LEFT])}, {get_addr(self.child[Direction.RIGHT])}],
}}"""

    def __repr__(self: Self) -> str:
        return f"{get_addr(self)} {{.value = {self.value}}}"

    def left(self: Self) -> Self | None:
        return self.child[Direction.LEFT]

    def right(self: Self) -> Self | None:
        return self.child[Direction.RIGHT]

    def is_leaf(self: Self) -> bool:
        return self.left() is None and self.right() is None

    def value_dir(self: Self, other: Self) -> Direction:
        return Direction.LEFT if self.value >= other.value else Direction.RIGHT

    def dir(self: Self, other: Self) -> Direction:
        return Direction.LEFT if self.left() is other else Direction.RIGHT

    def can_step(self: Self, direction: Direction) -> bool:
        return self.child[direction] is not None

    def tree_height(self: Self) -> int:
        def _tree_height(node: Self) -> int:
            left = node.left()
            right = node.right()

            return (
                max(
                    _tree_height(left) if left is not None else 0,
                    _tree_height(right) if right is not None else 0,
                )
                + 1
            )

        return _tree_height(self) - 1

    def rotate(self: Self, direction: Direction) -> Self:
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
            self.child[1 - direction].parent = self  # type: ignore

        child.child[direction] = self

        self.parent = child

        return child

    def insert(self: Self, other: Self) -> Self:
        current = self

        insert_direction: Direction = current.value_dir(other)

        while current.can_step(insert_direction):
            current = cast(Self, current.child[insert_direction])

            insert_direction = current.value_dir(other)

        other.parent = current

        current.child[insert_direction] = other

        return other

    def str_value(self: Self) -> str:
        return str(self.value)

    def draw(self: Self):
        height = self.tree_height()

        def calc_indent(height: int) -> int:
            return ((2 ** (height + 1)) - 1) // 2

        indent = calc_indent(height)

        final_queue: Deque[tuple[int, int, Self]] = deque()

        queue: Deque[tuple[int, int, int, Self]] = deque([(0, indent, height, self)])

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

        prev_indent, prev_level = 0, 0

        str_tree: str = ""

        while final_queue:
            (level, indent, node) = final_queue.popleft()

            if level > prev_level:
                str_tree, prev_level, prev_indent = str_tree + "\n", level, 0

            str_tree += f"{(' ' * cell_width) * (indent - prev_indent)}{node.str_value():0>{cell_width}}"

            prev_indent = indent + 1

        return str_tree


class AVLNode(Node):
    left_height: int
    right_height: int

    def __init__(self: Self, value: int):
        super().__init__(value)
        self.left_height = 0
        self.right_height = 0

    def str_value(self: Self) -> str:
        return f"{self.left_height}|{self.value}|{self.right_height}"

    def height_diff(self: Self) -> int:
        return self.left_height - self.right_height

    def update_heights(self: Self):
        if (left := self.left()) is None:
            self.left_height = 0
        else:
            self.left_height = 1 + max(left.left_height, left.right_height)

        if (right := self.right()) is None:
            self.right_height = 0
        else:
            self.right_height = 1 + max(right.left_height, right.right_height)

    def fix(self: Self) -> Self:
        current = self

        while current:
            current.update_heights()

            diff = current.height_diff()

            if diff > 1:  # left heavy
                left = cast(Self, current.left())

                if left.left_height >= left.right_height:
                    current.rotate(Direction.RIGHT)

                    # height updation
                    current.update_heights()
                    left.update_heights()

                    current = left
                else:
                    left_right = left.rotate(Direction.LEFT)

                    # height updation
                    left.update_heights()
                    left_right.update_heights()
                    current.update_heights()

                    current.rotate(Direction.RIGHT)

                    # height updation
                    current.update_heights()
                    left_right.update_heights()

                    current = left_right

            if diff < -1:  # right heavy
                right = cast(Self, current.right())

                if right.right_height >= right.left_height:
                    current.rotate(Direction.LEFT)

                    # height updation
                    current.update_heights()
                    right.update_heights()

                    current = right
                else:
                    right_left = right.rotate(Direction.RIGHT)

                    # height updation
                    right.update_heights()
                    right_left.update_heights()
                    current.update_heights()

                    current.rotate(Direction.LEFT)

                    # height updation
                    current.update_heights()
                    right_left.update_heights()

                    current = right_left

            if current.parent is None:
                root = current

            current = current.parent

        return cast(Self, root)

    def insert(self: Self, other: Self) -> Self:
        super().insert(other)

        return other.fix()

    @classmethod
    def create_instance(cls, value: int) -> Self:
        return cls(value)

    def insert_value(self: Self, value: int) -> Self:
        return self.insert(self.create_instance(value))


class Color(IntEnum):
    RED = 0
    BLACK = 1


class RedBlackNode(Node):
    color: Color

    def __init__(self: RedBlackNode, value: int):
        super().__init__(value)
        self.color = Color.BLACK

    def str_value(self: Self) -> str:
        return f"{'R' if self.color == Color.RED else 'B'}{self.value}"

    def fix(self: Self) -> Self:
        current = self

        parent = current.parent

        while parent is not None and parent.color != Color.BLACK:
            current.update_heights()

            diff = current.height_diff()

            if diff > 1:  # left heavy
                left = cast(Self, current.left())

                if left.left_height >= left.right_height:
                    current.rotate(Direction.RIGHT)

                    # height updation
                    current.update_heights()
                    left.update_heights()

                    current = left
                else:
                    left_right = left.rotate(Direction.LEFT)

                    # height updation
                    left.update_heights()
                    left_right.update_heights()
                    current.update_heights()

                    current.rotate(Direction.RIGHT)

                    # height updation
                    current.update_heights()
                    left_right.update_heights()

                    current = left_right

            if diff < -1:  # right heavy
                right = cast(Self, current.right())

                if right.right_height >= right.left_height:
                    current.rotate(Direction.LEFT)

                    # height updation
                    current.update_heights()
                    right.update_heights()

                    current = right
                else:
                    right_left = right.rotate(Direction.RIGHT)

                    # height updation
                    right.update_heights()
                    right_left.update_heights()
                    current.update_heights()

                    current.rotate(Direction.LEFT)

                    # height updation
                    current.update_heights()
                    right_left.update_heights()

                    current = right_left

            if current.parent is None:
                root = current

            current = current.parent

        return cast(Self, root)

    def insert(self: Self, other: Self) -> Self:
        super().insert(other)

        return other.fix()

    @classmethod
    def create_instance(cls, value: int) -> Self:
        return cls(value)

    def insert_value(self: Self, value: int) -> Self:
        return self.insert(self.create_instance(value))


def example():
    root = AVLNode(10)
    root = root.insert_value(20)
    root = root.insert_value(30)
    print(root.draw())
    root = root.insert_value(40)
    root = root.insert_value(5)
    root = root.insert_value(-10)
    return root
