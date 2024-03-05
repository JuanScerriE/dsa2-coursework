from random import randint

def swap(lst: list[int], i: int, j: int) -> None:
    temp = lst[i]
    lst[i] = lst[j]
    lst[j] = temp

# https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle#The_modern_algorithm

def shuffle(lst: list[int]) -> list[int]:
    for i in range(len(lst) - 1, 0, -1):
        j = randint(0, i)
        swap(lst, i, j)

    return lst
