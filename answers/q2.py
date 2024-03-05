def merge(a, b):
    i = 0
    j = 0

    c = []

    while i < len(a) or j < len(b):
        if j == len(b) or (i < len(a) and a[i] <= b[j]):
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1

    return c
