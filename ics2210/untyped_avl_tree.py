#!/usr/bin/env python3

from .untyped_tree import Direction, Node, Tree

from statistics import mean, median, variance

from random import randint, seed


class AVLNode(Node):
    left_height: int
    right_height: int

    def __init__(self, value: int):
        super().__init__(value)
        self.left_height = 0
        self.right_height = 0

    def height_diff(self) -> int:
        return self.left_height - self.right_height

    def update_heights(self):
        if (left := self.left()) is None:
            self.left_height = 0
        else:
            self.left_height = 1 + max(left.left_height, left.right_height)

        if (right := self.right()) is None:
            self.right_height = 0
        else:
            self.right_height = 1 + max(right.left_height, right.right_height)


class AVLTree(Tree):
    num_of_rotations: list[int]

    def __init__(self, enable_stats: bool = False):
        super().__init__(enable_stats=enable_stats)

        if self.enable_stats:
            self.num_of_rotations = []

    def fix(self, node):
        current = node

        if self.enable_stats:
            rotations = 0

        while current:
            current.update_heights()

            diff = current.height_diff()

            if diff > 1:  # left heavy
                left = current.left()

                if left.left_height >= left.right_height:
                    current.rotate(Direction.RIGHT)

                    # height updation
                    current.update_heights()
                    left.update_heights()

                    current = left

                    if self.enable_stats:
                        rotations += 1
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

                    if self.enable_stats:
                        rotations += 1

            if diff < -1:  # right heavy
                right = current.right()

                if right.right_height >= right.left_height:
                    current.rotate(Direction.LEFT)

                    # height updation
                    current.update_heights()
                    right.update_heights()

                    current = right

                    if self.enable_stats:
                        rotations += 1
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

                    if self.enable_stats:
                        rotations += 1

            if current.parent is None:
                root = current

            current = current.parent

        if self.enable_stats:
            self.num_of_rotations.append(rotations)

        return root

    def insert(self, node):
        self.root = self.fix(super().insert(node))

    def insert_value(self, value):
        self.insert(AVLNode(value))

    def compute_stats(self):
        if not self.enable_stats:
            return

        min_steps = min(self.num_of_steps)
        max_steps = max(self.num_of_steps)
        mean_steps = mean(self.num_of_steps)
        variance_steps = variance(self.num_of_steps)
        median_steps = median(self.num_of_steps)

        print(
            f"""Min Steps: {min_steps}
Max Steps: {max_steps}
Mean Steps: {mean_steps}
Variance Steps: {variance_steps}
Median Step: {median_steps}"""
        )

        min_rotations = min(self.num_of_rotations)
        max_rotations = max(self.num_of_rotations)
        mean_rotations = mean(self.num_of_rotations)
        variance_rotations = variance(self.num_of_rotations)
        median_rotations = median(self.num_of_rotations)

        print(
            f"""Min Rotations: {min_rotations}
Max Rotations: {max_rotations}
Mean Rotations: {mean_rotations}
Variance Rotations: {variance_rotations}
Median Rotations: {median_rotations}"""
        )

        print(f"Height: {self.calc_height()}")

        print(f"Leaves: {self.calc_leaves()}")


def example():
    tree = AVLTree(enable_stats=True)

    seed(10)

    for _ in range(20):
        tree.insert_value(randint(1, 50))

    tree.draw()
    tree.compute_stats()

    return tree
