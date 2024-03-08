from __future__ import annotations

from enum import IntEnum
from collections import deque
from typing import cast, Self, Any, Deque


def get_addr(object: Any) -> str:
    return "None" if object is None else str(id(object))


class Direction(IntEnum):
    LEFT = 0
    RIGHT = 1

    @staticmethod
    def from_int(value: int) -> Direction:
        return Direction.LEFT if value <= 0 else Direction.RIGHT


class Node:
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
        return Direction.LEFT if self.value > other.value else Direction.RIGHT

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
