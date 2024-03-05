import answers.q9 as q9

# Three arrays and there expected duplicates are defined. The
# result of the algorithm is compared to the expected output.

print("Finding Duplicates Tests")

if [1, 2, 3] == q9.find_dups([1, 1, 2, 3, 4, 5, 6, 2, 3, 3, 2, 1, 1, 48, 23]):
    print("Test Passed")
else:
    print("Test Failed")

if [1, 2, 3, 45] == q9.find_dups(
    [1, 1, 2, 3, 4, 5, 6, 2, 3, 3, 2, 1, 1, 48, 23, 45, 45]
):
    print("Test Passed")
else:
    print("Test Failed")

if [1, 2, 3, -12] == q9.find_dups(
    [1, 1, 2, 3, 4, 5, 6, 2, 3, 3, 2, 1, 1, 48, 23, -12, -12]
):
    print("Test Passed")
else:
    print("Test Failed")
