from __future__ import annotations

from .bs_tree import Node, Direction
from enum import IntEnum
from typing import cast, Self


def is_black(node: RedBlackNode | None) -> bool:
    return (node is None) or (node.color == Color.BLACK)


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

    def sibling_is_red(self: Self) -> bool:
        parent = cast(Self, self.parent)  # assuming the parent exists

        return not is_black(parent.child[1 - parent.dir(self)])

    def get_sibling(self: Self) -> Self | None:
        parent = cast(Self, self.parent)  # assuming the parent exists

        return parent.child[1 - parent.dir(self)]

    def fix(self: Self) -> Self:
        current = self

        parent = current.parent

        while not is_black(parent):
            parent = cast(
                Self, parent
            )  # parent is definitely not None due to check in is_black

            grandparent = cast(
                Self, parent.parent
            )  # grandparent exists since parent is red

            if parent.sibling_is_red():
                sibling = cast(
                    Self, parent.get_sibling()
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

                    return parent
                else:
                    parent.rotate(Direction.from_int(1 - direction))
                    grandparent.rotate(Direction.from_int(1 - parent_direction))

                    current.color = Color.BLACK
                    grandparent.color = Color.RED

                    return current

            current, parent = grandparent, grandparent.parent

        return current

    def insert(self: Self, other: Self) -> Self:
        other.color = Color.RED  # always insert as RED

        super().insert(other)

        node = other.fix()

        return node if (node.parent is None) else self

    @classmethod
    def create_instance(cls, value: int) -> Self:
        return cls(value)

    def insert_value(self: Self, value: int) -> Self:
        return self.insert(self.create_instance(value))


def exampleRedBlack():
    root = RedBlackNode(10)
    root = root.insert_value(20)
    root = root.insert_value(30)
    root.draw()
    root = root.insert_value(40)
    root = root.insert_value(5)
    root = root.insert_value(-10)
    root.draw()
    return root
