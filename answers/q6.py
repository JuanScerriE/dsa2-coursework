import math


# The idea: Basically, entails the creation of an array whose
# size is determined by the input, in this case `limit`. The
# array will be filled with `True` or `False`. `True` denotes
# that the index used to access that location in the array is a
# prime. `False` denotes that the index used to access that
# location is not prime. The first two indices 0 and 1 are not
# prime and they are set to `False`.
#
# Starting from index 2, if the value at index n is `True` then
# mark every multiple of n (2n, 3n, 4n, ...) except n itself, as
# `False` up till the limit. Repeat the process for all other
# indices.
#
# At the end you will have effectively struck out all the
# indices which are not prime.

# Optimisation 1: The initial pattern is usually [False, False,
# True, True, True, ...]. Instead we can start with [False,
# False, True, False, True, False, True, False, ...]. This means
# that we are already discounting half of the array.
#
# This is valid because the pattern coincides with the pattern
# of even and odd numbers. As we know every even number which is
# not 2 is not prime.

# Optimisation 2: There is no need to check every element until
# the limit is reached. Checking up till the square root of the
# limit is enough to find all prime numbers up till the limit.
#
# This is possible because composite numbers smaller than the
# limit will have at least one prime factor which is smaller
# than or equal to their own square root.
#
# Hence, all composite numbers smaller than the limit will have
# at least one prime factor which is smaller than or equal to
# the square root of the limit. (p <= q <=> sqrt(p) <= sqrt(q))

# Optimisation 3: Start by crossing out from the square of the
# index (n^2) instead of the index (n).
#
# This is because anything smaller than the square of our index
# is either prime or has at least one prime factor which is
# smaller than the index (n - 1 = floor(sqrt(n^2 - 1))).
# Therefore, it would have already been marked since the
# procedure for all numbers up till n (including n - 1) would
# have already been completed.
#
# Again this uses the same property as Optimisation 2.


def f_sieve(limit):
    # Optimisation 1
    N = [False, True] * ((limit + 1) // 2)

    N[1] = False
    N[2] = True

    # Optimisation 2
    for n in range(3, int(math.ceil(math.sqrt(limit))), 2):
        if N[n]:
            # Optimisation 3
            for m in range(n * n, limit, n):
                N[m] = False

    P = []

    for n in range(limit):
        if N[n]:
            P.append(n)

    return P


def is_prime(n):
    if n <= 1:
        return False

    if n == 2:
        return True

    # We check if it is even and not 2. If so then is it is
    # definitely not prime.
    if n % 2 == 0:
        return False

    # There is at least one prime factor of n which is smaller
    # than or equal to the sqrt(n).
    for i in range(2, int(math.ceil(math.sqrt(n)))):
        if n % i == 0:
            return False

    return True
