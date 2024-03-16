#!/usr/bin/env python3

from random import seed, randint

from ics2210.knuth_shuffling import shuffle
from ics2210.untyped_avl_tree import AVLTree
from ics2210.untyped_rb_tree import RBTree
from ics2210.skip_list import SkipList

seed()

permutation = [n for n in range(1, 5000 + 1, 1)]

shuffle(permutation)

avl_tree = AVLTree(enable_stats=True)

for value in permutation:
    avl_tree.insert_value(value)

print("AVL Tree Stats:")
avl_tree.compute_stats()
print()
# avl_tree.draw()
# print()

rb_tree = RBTree(enable_stats=True)

for value in permutation:
    rb_tree.insert_value(value)

print("RB Tree Stats:")
rb_tree.compute_stats()
print()
# rb_tree.draw()
# print()

skip_list = SkipList(enable_stats=True)

for value in permutation:
    skip_list.insert(value)

print("Skip List Stats:")
skip_list.compute_stats()
print()
# skip_list.draw()
# print()

other_array = [randint(0, 100000) for _ in range(1000)]

for value in other_array:
    avl_tree.insert_value(value)

print("AVL Tree Stats:")
avl_tree.compute_stats()
print()

for value in other_array:
    rb_tree.insert_value(value)

print("RB Tree Stats:")
rb_tree.compute_stats()
print()

for value in other_array:
    skip_list.insert(value)

print("Skip List Stats:")
skip_list.compute_stats()
print()
