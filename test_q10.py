import answers.q10 as q10

# A number of arrays are defined along with there expected
# output. The expected output is compared to the actual result.

print("`max` Tests\n")

if [88] == q10.max([88, 14, 1, 3, 7, 21, 59]):
    print("Test Passed")
else:
    print("Test Failed")


if [59] == q10.max([13, 14, 1, 3, 7, 5, 21, 59]):
    print("Test Passed")
else:
    print("Test Failed")

print("\n`max_2` Tests\n")

if 88 == q10.max_2([88, 14, 1, 3, 7, 21, 59]):
    print("Test Passed")
else:
    print("Test Failed")

if 59 == q10.max_2([13, 14, 1, 3, 7, 5, 21, 59]):
    print("Test Passed")
else:
    print("Test Failed")

print("\n`max` Implementation\n")

print("max([13,14,1,3,7,5,21,59]) = " + str(q10.max([13, 14, 1, 3, 7, 5, 21, 59])))
print("max([88,14,1,3,7,21,59]) = " + str(q10.max([88, 14, 1, 3, 7, 21, 59])))
print(
    "max([13,-1214,1,3,7,5,21,59]) = " + str(q10.max([13, -1214, 1, 3, 7, 5, 21, 59]))
)
print(
    "max([13,14,1,12,34,123,3,7,5,21,59]) = "
    + str(q10.max([13, 14, 1, 12, 34, 123, 3, 7, 5, 21, 59]))
)

print("\n`max_2` Implementation\n")

print("max_2([13,14,1,3,7,5,21,59]) = " + str(q10.max_2([13, 14, 1, 3, 7, 5, 21, 59])))
print("max_2([88,14,1,3,7,21,59]) = " + str(q10.max_2([88, 14, 1, 3, 7, 21, 59])))
print(
    "max_2([13,-1214,1,3,7,5,21,59]) = "
    + str(q10.max_2([13, -1214, 1, 3, 7, 5, 21, 59]))
)
print(
    "max_2([13,14,1,12,34,123,3,7,5,21,59]) = "
    + str(q10.max_2([13, 14, 1, 12, 34, 123, 3, 7, 5, 21, 59]))
)
