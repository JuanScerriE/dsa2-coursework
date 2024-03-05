# This is a very compact recursive algorithm for finding the
# maximum, inspired by merge sort. The first implementation
# `max` returns a singleton with the largest element of the
# provided list. However, it has three recursive calls instead
# of two.

# `max_2` is similar to `max` it however eliminates the need for
# the third recursive call.


def max(list):
    if len(list) == 1:
        return [list[0]]
    elif len(list) == 2:
        return [list[0]] if list[0] > list[1] else [list[1]]
    else:
        return max(max(list[: len(list) // 2]) + max(list[len(list) // 2 :]))


def half(list):
    return list[: len(list) // 2], list[len(list) // 2 :]


def max_2(list):
    if len(list) == 1:
        return list[0]
    elif len(list) == 2:
        return list[0] if list[0] > list[1] else list[1]
    else:
        list_u, list_l = half(list)

        u = max_2(list_u)
        l = max_2(list_l)

        return u if u > l else l
