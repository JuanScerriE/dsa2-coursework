from __future__ import annotations

from typing import cast, Self, Literal
from statistics import mean, median, variance
from random import randint, seed


class Integer:
    value: int | Literal["-inf", "inf"]

    def __init__(self: Self, value: int | Literal["-inf", "inf"]):
        self.value = value

    def __eq__(self: Self, other: Self) -> bool:
        return self.value == other.value

    def __lt__(self: Self, other: Self) -> bool:
        if type(self.value) == int and type(other.value) == int:
            return self.value < other.value

        if self.value == "-inf" and other.value != "-inf":
            return True

        if other.value == "inf" and other.value != "inf":
            return True

        return False

    def __le__(self: Self, other: Self) -> bool:
        return self < other or self == other

    def __gt__(self: Self, other: Self) -> bool:
        return other < self

    def __ge__(self: Self, other: Self) -> bool:
        return other < self or other == self

    def __repr__(self: Self) -> str:
        return f"{self.value}"


class SkipNode:
    value: Integer
    forward: list[Self | None]

    def __init__(self: Self, value: Integer):
        self.value = value
        self.forward = [None]

    @classmethod
    def head(cls) -> Self:
        return cls(Integer("-inf"))

    @classmethod
    def tail(cls) -> Self:
        return cls(Integer("inf"))

    def add(self: Self, other: Self, level: int):
        forward = self.forward[level]

        self.forward[level] = other

        if level < len(other.forward):
            other.forward[level] = forward
        else:
            other.forward.append(forward)

    def add_level(self: Self):
        self.forward.append(None)

    def __repr__(self: Self) -> str:
        return str(self.value)


class SkipList:
    head: SkipNode
    tail: SkipNode
    height: int
    length: int
    enable_stats: bool
    num_of_steps: list[int]
    num_of_promotions: list[int]

    def __init__(self: Self, enable_stats: bool = False):
        self.head = SkipNode.head()
        self.tail = SkipNode.tail()
        self.height = 0
        self.length = 2
        self.head.forward[self.height] = self.tail
        self.enable_stats = enable_stats

        if enable_stats:
            self.num_of_steps = []
            self.num_of_promotions = []

    def add_level(self: Self):
        self.height += 1

        self.head.add_level()
        self.tail.add_level()

        self.head.forward[self.height] = self.tail

    def insert(self: Self, value: int):
        self.length += 1

        integer = Integer(value)

        current_height = self.height

        current = self.head

        stack = []

        if self.enable_stats:
            steps = 0

        while current_height > 0:
            while integer >= cast(SkipNode, current.forward[current_height]).value:
                current = cast(SkipNode, current.forward[current_height])

                if self.enable_stats:
                    steps += 1

            stack.append(current)

            current_height -= 1

        while integer >= cast(SkipNode, current.forward[current_height]).value:
            current = cast(SkipNode, current.forward[current_height])

            if self.enable_stats:
                steps += 1

        new_element = SkipNode(integer)

        current.add(new_element, current_height)

        if self.enable_stats:
            promotions = 0

        while randint(0, 1) == 0:  # add level
            if self.enable_stats:
                promotions += 1

            current_height += 1

            if stack:  # i.e. it is not empty
                current = stack.pop()

                current.add(new_element, current_height)
            else:
                self.add_level()

                self.head.add(new_element, current_height)

        if self.enable_stats:
            self.num_of_steps.append(steps)
            self.num_of_promotions.append(promotions)

    def draw(self: Self):
        cell_width = 0

        current = cast(SkipNode, self.head)

        offsets: dict[SkipNode, int] = {}

        for i in range(self.length):
            cell_width = max(len(str(current.value)), cell_width)

            offsets[current] = i

            current = cast(SkipNode, current.forward[0])

        level_cell_width = len(str(self.height))

        print("Length:", self.length)

        for level in range(self.height, -1, -1):
            current = self.head

            print(f"Level {level: >{level_cell_width}}: ", end="")

            prev_offset = 0

            while current is not None:
                offset = offsets[current]

                print(
                    f"{(' ' * (cell_width + 1)) * (offset - prev_offset)}{str(current.value): >{cell_width}},",
                    end="",
                )

                prev_offset = offset + 1

                current = current.forward[level]

            print()

    def compute_stats(self: Self):
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

        min_promotions = min(self.num_of_promotions)
        max_promotions = max(self.num_of_promotions)
        mean_promotions = mean(self.num_of_promotions)
        variance_promotions = variance(self.num_of_promotions)
        median_promotions = median(self.num_of_promotions)

        print(
            f"""Min Promotions: {min_promotions}
Max Promotions: {max_promotions}
Mean Promotions: {mean_promotions}
Variance Promotions: {variance_promotions}
Median Promotions: {median_promotions}"""
        )

        levels = self.height + 1

        print(f"Levels: {levels}")


def exampleSkipList():
    skip_list = SkipList()

    seed(10)

    for _ in range(20):
        skip_list.insert(randint(1, 50))

    skip_list.draw()
    skip_list.compute_stats()

    return skip_list


def exampleSkipListWithStats():
    skip_list = SkipList(enable_stats=True)

    seed(10)

    for _ in range(20):
        skip_list.insert(randint(1, 50))

    skip_list.draw()
    skip_list.compute_stats()

    return skip_list
