from __future__ import annotations

from enum import IntEnum

class Branch(IntEnum):
    LEFT = 0
    ROOT = 1
    RIGHT = 2

class Direction(IntEnum):
    LEFT = 0
    RIGHT = 1


def value_direction(node: Node, other: Node) -> Direction:
    return Direction.LEFT if node.value > other.value else Direction.RIGHT 

def can_step(node: Node, direction: Direction) -> bool:
    return node.child[direction] is not None

class Node:
    value: int
    parent: Node | None
    child: list[Node | None]

    def __init__(self: Node, value: int) -> None:
        self.value = value
        self.parent = None
        self.child = [None, None]

    def insert(self: Node, other: Node) -> Node:
        current: Node = self 

        insert_direction: Direction = value_direction(current, other) 
        
        while can_step(current, insert_direction):
            current = current.child[insert_direction] # type: ignore

            insert_direction = value_direction(current, other)

        other.parent = current

        current.child[insert_direction] = other

        return other

    def insert_value(self: Node, value: int) -> Node:
        return self.insert(Node(value))

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
        super(value)
        left_height = 0
        right_height = 0


class RedBlackNode(Node):
    pass
