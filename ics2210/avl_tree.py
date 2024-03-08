from __future__ import annotations
from .bs_tree import Node, Direction

from typing import cast, Self


class AVLNode(Node):
    left_height: int
    right_height: int

    def __init__(self: Self, value: int):
        super().__init__(value)
        self.left_height = 0
        self.right_height = 0

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


class AVLTree:
    root: AVLNode | None
    height: int
    leaves: int
    enable_stats: bool
    num_of_steps: list[int]
    num_of_rotations: list[int]

    def __init__(self: Self, enable_stats: bool = False):
        self.root = None
        self.height = 0
        self.leaves = 0
        self.enable_stats = enable_stats

        if enable_stats:
            self.num_of_steps = []
            self.num_of_rotations = []


def exampleAVL():
    root = AVLNode(10)
    root = root.insert_value(20)
    root = root.insert_value(30)
    root.draw()
    root = root.insert_value(40)
    root = root.insert_value(5)
    root = root.insert_value(-10)
    root.draw()
    return root
