from __future__ import annotations

from enum import IntEnum
from collections import deque
from random import randint
from typing import cast, Self, Any, Deque, Literal


def get_addr(object: Any) -> str:
    return "None" if object is None else str(id(object))


class Direction(IntEnum):
    LEFT = 0
    RIGHT = 1

    @staticmethod
    def from_int(value: int) -> Direction:
        return Direction.LEFT if value <= 0 else Direction.RIGHT


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


def exampleAVL():
    root = AVLNode(10)
    root = root.insert_value(20)
    root = root.insert_value(30)
    root.draw()
    root = root.insert_value(40)
    root = root.insert_value(5)
    root = root.insert_value(-10)
    return root


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
    return root


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

    def __init__(self: Self):
        self.head = SkipNode.head()
        self.tail = SkipNode.tail()
        self.height = 0
        self.length = 2
        self.head.forward[self.height] = self.tail

    def find(self: Self, value: int) -> tuple[SkipNode, bool]:
        integer = Integer(value)

        current_height = self.height

        current = self.head

        while current_height > 0:
            while integer >= cast(SkipNode, current.forward[current_height]).value:
                current = cast(SkipNode, current.forward[current_height])

            current_height -= 1

        while integer >= cast(SkipNode, current.forward[current_height]).value:
            current = cast(SkipNode, current.forward[current_height])

        return current, current.value == integer

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

        while current_height > 0:
            while integer >= cast(SkipNode, current.forward[current_height]).value:
                current = cast(SkipNode, current.forward[current_height])

            stack.append(current)

            current_height -= 1

        while integer >= cast(SkipNode, current.forward[current_height]).value:
            current = cast(SkipNode, current.forward[current_height])

        new_element = SkipNode(integer)

        current.add(new_element, current_height)

        while randint(0, 1) == 0:  # add level
            current_height += 1

            if stack:  # i.e. it is not empty
                current = stack.pop()

                current.add(new_element, current_height)
            else:
                self.add_level()

                self.head.add(new_element, current_height)

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


def exampleSkipList():
    skiplist = SkipList()
    skiplist.insert(20)
    skiplist.insert(30)
    skiplist.draw()
    skiplist.insert(40)
    skiplist.insert(5)
    skiplist.insert(-10)
    return skiplist
