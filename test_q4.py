import answers.q4 as q4
import random

# An array and its expected product equalities are defined. The
# expected result is then compared to the actual result.

print("Finding Products Test")

test_related = q4.find_products([1, 5, 3, 6, 8, 7, 15, 9])

expected_related = [
    (q4.ProductTriple(1, 15), q4.ProductTriple(3, 5)),
    (q4.ProductTriple(3, 15), q4.ProductTriple(5, 9)),
]

pass_test = True

for i in range(len(test_related)):
    if not (
        expected_related[i][0].equals(test_related[i][0])
        and expected_related[i][1].equals(test_related[i][1])
    ):
        pass_test = False

if pass_test:
    print("Test Passed\n")
else:
    print("Test Failed\n")

a = [random.randint(1, 1024) for k in range(64)]
# a = [1,2,4,6,12,24]

related = q4.find_products(a)

# The found product equalities are printed. This allows for
# further checking.

for pair in related:
    if not pair[0].product_equals(pair[1]):
        print("!Failed! ", end="")

    print(
        pair[0].a,
        "*",
        pair[0].b,
        "( =",
        pair[0].ab,
        ")",
        "=",
        pair[1].a,
        "*",
        pair[1].b,
        "(=",
        pair[1].ab,
        ")",
    )
