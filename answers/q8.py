# For this solution I used a well-known method developed by
# Newton to find approximate solutions for the roots of
# equations. Specifically, I used the method to derive an
# approximation for the root of y = x^2 - c. This means solving
# for y = 0 i.e. 0 = x^2 - c => sqrt(c) = x. Hence, by solving
# the following equation an approximation for the sqrt(c) is
# found.

# In this case the algorithm has a time-complexity of O(n) where
# n depends on the input.
#
# Iteration is needed to ensure that the approximation is
# reasonably accurate.
#
# If the domain of the function was bounded, the algorithm could
# be made O(1) by always making the function iterate a
# sufficient number of times for all the values in the given
# domain.


import math


# This function is the actual answer.
def newton_sqrt(n):
    if n < 0:
        return -1

    x = n

    for i in range(max(math.floor(n), 5)):
        x = x - (x**2 - n) / (2 * x)

    return x


# This is an interesting optimisation (increasing the rate at
# which the function converges) Although I do not think this
# would be a practical optimisation because the mathematical
# computation is much more expensive.
def halley_sqrt(n):
    if n < 0:
        return -1

    x = n

    for i in range(math.floor(n)):
        x = x - (2 * (x**2 - n) * (2 * x)) / (8 * (x**2) - 2 * (x**2 - n))

    return x
