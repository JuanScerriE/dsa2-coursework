#!/usr/bin/env python3

from random import seed, randint
from statistics import mean

import time

from ics2210.untyped_avl_tree import AVLTree
from ics2210.untyped_rb_tree import RBTree
from ics2210.skip_list import SkipList

seed()

# check how long it takes to insert a set
# of 10,000 elements a 100 times over.

# we are doing each test multiple times
# instead of once to ensure that the initial
# result is not an exception

insertion_times = []

find_times = []

for _ in range(100):
    array = (randint(0, 100000) for _ in range(10000))

    avl_tree = AVLTree()

    start = time.time()

    for value in array:
        avl_tree.insert_value(value)

    end = time.time()

    insertion_times.append(end - start)

    array = (randint(0, 100000) for _ in range(10000))

    start = time.time()

    for value in array:
        avl_tree.find(value)

    end = time.time()

    find_times.append(end - start)


print(f"AVL Tree Insertion Average: {mean(insertion_times)}s")
print(f"AVL Tree Find Average: {mean(find_times)}s")

insertion_times.clear()

find_times.clear()

for _ in range(100):
    array = (randint(0, 100000) for _ in range(10000))

    rb_tree = RBTree()

    start = time.time()

    for value in array:
        rb_tree.insert_value(value)

    end = time.time()

    insertion_times.append(end - start)

    array = (randint(0, 100000) for _ in range(10000))

    start = time.time()

    for value in array:
        rb_tree.find(value)

    end = time.time()

    find_times.append(end - start)

print(f"Red-Black Tree Insertion Average: {mean(insertion_times)}s")
print(f"Red-Black Tree Find Average: {mean(find_times)}s")

insertion_times.clear()

find_times.clear()

for _ in range(100):
    array = (randint(0, 100000) for _ in range(10000))

    skip_list = SkipList()

    start = time.time()

    for value in array:
        skip_list.insert(value)

    end = time.time()

    insertion_times.append(end - start)

    array = (randint(0, 100000) for _ in range(10000))

    start = time.time()

    for value in array:
        skip_list.find(value)

    end = time.time()

    find_times.append(end - start)


print(f"Skip List Insertion Average: {mean(insertion_times)}s")
print(f"Skip List Find Average: {mean(find_times)}s")

