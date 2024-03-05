import math
import random


def swap(a, x, y):
    t = a[x]
    a[x] = a[y]
    a[y] = t


# General term of the gap sequence.
# Proposed by Frank & Lazarus.
def next_h(h):
    return 2 * int(math.floor(h / 4)) + 1


def shellsort(a):
    n = len(a)
    h = next_h(n)

    while h >= 1:
        for i in range(h):
            # Modified insertion sort to
            # deal with gaps of size h.
            for j in range(i + h, n, h):
                for k in range(j, i, -h):
                    if a[k] < a[k - h]:
                        swap(a, k, k - h)
                    else:
                        break

        if h == 1:
            break

        h = next_h(h)

    return a


# Collecting a random distribution of 7 elements, sorting them
# using shellsort and returning the median of the sorted list.
# The execution time is constant, hence it has a time-complexity
# of O(1).
def pivot(a, i, j):
    n = []

    for k in [random.randint(i, j) for k in range(7)]:
        n.append(a[k])

    shellsort(n)

    return n[3]


# The partitioning scheme being used is the Hoare partitioning
# scheme.
def partition(a, i, j):
    p = pivot(a, i, j)
    i -= 1
    j += 1

    while True:
        while True:
            i += 1
            if a[i] >= p:
                break

        while True:
            j -= 1
            if a[j] <= p:
                break

        if i >= j:
            return i

        swap(a, i, j)


def quicksort(a, i, j):
    if 0 <= i and 0 <= j and i < j:
        p = partition(a, i, j)
        quicksort(a, i, p - 1)
        quicksort(a, p, j)
