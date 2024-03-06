from __future__ import annotations

from enum import IntEnum

from typing import Any


class Branch(IntEnum):
    LEFT = 0
    ROOT = 1
    RIGHT = 2


class Direction(IntEnum):
    LEFT = 0
    RIGHT = 1


def value_dir(node: Node, other: Node) -> Direction:
    return Direction.LEFT if node.value > other.value else Direction.RIGHT


def dir(node: Node, other: Node) -> Direction:
    return Direction.LEFT if node.child[Direction.LEFT] is other else Direction.RIGHT


def can_step(node: Node, direction: Direction) -> bool:
    return node.child[direction] is not None


def get_addr(object: Any) -> str:
    return "None" if object is None else str(id(object))


class Node:
    value: int
    parent: Node | None
    child: list[Node | None]

    def __init__(self: Node, value: int):
        self.value = value
        self.parent = None
        self.child = [None, None]

    def __str__(self: Node) -> str:
        return f"""{get_addr(self)} {{
  .value = {self.value},
  .parent = {get_addr(self.parent)},
  .child = [{get_addr(self.child[Direction.LEFT])}, {get_addr(self.child[Direction.RIGHT])}],
}}"""

    def rotate(self: Node, direction: Direction) -> Node:
        child = self.child[1 - direction]

        if child is None:
            return self

        if self.parent is None:
            child.parent = None
        else:
            child.parent = self.parent

            self.parent.child[dir(self.parent, self)] = child

        self.child[1 - direction] = child.child[direction]

        if self.child[1 - direction] is not None:
            self.child[1 - direction].parent = self  # type: ignore

        child.child[direction] = self

        self.parent = child

        return child

    def insert(self: Node, other: Node) -> Node:
        current: Node = self

        insert_direction: Direction = value_dir(current, other)

        while can_step(current, insert_direction):
            current = current.child[insert_direction]  # type: ignore

            insert_direction = value_dir(current, other)

        other.parent = current

        current.child[insert_direction] = other

        return other

    def insert_value(self: Node, value: int) -> Node:
        return self.insert(Node(value))

    # TODO: pick a better method for printing

    def value_format(self: Node) -> str:
        return str(self.value)

    def draw(self: Node, s: str = "", parent: Branch = Branch.ROOT):
        if self.child[Direction.RIGHT] is not None:
            if parent == Branch.RIGHT or parent == Branch.ROOT:
                self.child[Direction.RIGHT].draw(
                    s[: (len(s) - 1)] + " " + " " * len(self.value_format()) + " |",
                    Branch.RIGHT,
                )
                print(s[: (len(s) - 1)] + " " + " " * len(self.value_format()) + "/")
            else:
                self.child[Direction.RIGHT].draw(
                    s[: (len(s) - 1)] + "|" + " " * len(self.value_format()) + " |",
                    Branch.RIGHT,
                )
                print(s[: (len(s) - 1)] + "\\" + " " * len(self.value_format()) + "/")

        print(s[: (len(s) - 1)] + " " + self.value_format())

        if self.child[Direction.LEFT] is not None:
            if parent == Branch.LEFT or parent == Branch.ROOT:
                print(s[: (len(s) - 1)] + " " + " " * len(self.value_format()) + "\\")
                self.child[Direction.LEFT].draw(
                    s[: (len(s) - 1)] + " " + " " * len(self.value_format()) + " |",
                    Branch.LEFT,
                )
            else:
                print(s[: (len(s) - 1)] + "/" + " " * len(self.value_format()) + "\\")
                self.child[Direction.LEFT].draw(
                    s[: (len(s) - 1)] + "|" + " " * len(self.value_format()) + " |",
                    Branch.LEFT,
                )


class AVLNode(Node):
    left_height: int
    right_height: int

    def __init__(self: AVLNode, value: int):
        super().__init__(value)
        self.left_height = 0
        self.right_height = 0


class Color(IntEnum):
    RED = 0
    BLACK = 1


class RedBlackNode(Node):
    color: Color

    def __init__(self: RedBlackNode, value: int):
        super().__init__(value)
        self.color = Color.BLACK
