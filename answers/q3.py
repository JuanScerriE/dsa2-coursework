def extremes(a):
    sorted = True
    ret = []

    for i in range(1, len(a) - 1):
        if (a[i] > a[i + 1] and a[i] > a[i - 1]) or (
            a[i] < a[i + 1] and a[i] < a[i - 1]
        ):
            sorted = False
            print(a[i], end=" ")
            ret.append(a[i])

    if sorted:
        # See explanation as to why this is the case in the
        # report.
        print("SORTED")
    else:
        print()

    return ret
