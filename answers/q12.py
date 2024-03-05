# I am using the closed-form expression for the Fibonacci
# Sequence to get the exact value at index n without having to
# compute all the previous elements of the sequence. Albeit, I
# am using rounding which is a slight optimisation.

# Moreover, I am using the closed-form expression for the sum of
# the elements in the sequence to get the exact sum at index n
# without having to add all previous elements. This makes the
# algorithm's time-complexity O(1).

import math


def fib(n):
    return round((((1 + math.sqrt(5)) / 2) ** n) / math.sqrt(5))


def sum_fib(n):
    return fib(n + 2) - 1
