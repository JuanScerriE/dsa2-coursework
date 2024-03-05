# I am using the first 7 non-zero terms of the Maclaurin
# expansion for sine. The sine function is a periodic function
# with a fundamental period of 2pi. Therefore, we can take any
# real number and compute its equivalent in the range -pi and
# pi. This allows us to find the value of the sine function for
# any real number.

import math


def sin(x):
    while x < -math.pi or x > math.pi:
        if x >= 0:
            x -= 2 * math.pi
        else:
            x += 2 * math.pi

    return (
        x
        - (x**3) / 6
        + (x**5) / 120
        - (x**7) / 5040
        + (x**9) / 362880
        - (x**11) / 39916800
        + (x**13) / 6227020800
    )


def cos(x):
    return sin(x + math.pi / 2)
