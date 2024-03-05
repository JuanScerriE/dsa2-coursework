import answers.q8 as q8

# Again the results of the algorithms are compared to the
# expected results up to 4 decimal places.

print("Newton Tests\n")

if 1.4142 == round(q8.newton_sqrt(2), 4):
    print("Test Passed")
else:
    print("Test Failed")

if 2.2361 == round(q8.newton_sqrt(5), 4):
    print("Test Passed")
else:
    print("Test Failed")

if 3.1623 == round(q8.newton_sqrt(10), 4):
    print("Test Passed")
else:
    print("Test Failed")

print("\nHalley Tests\n")

if 1.4142 == round(q8.halley_sqrt(2), 4):
    print("Test Passed")
else:
    print("Test Failed")

if 2.2361 == round(q8.halley_sqrt(5), 4):
    print("Test Passed")
else:
    print("Test Failed")

if 3.1623 == round(q8.halley_sqrt(10), 4):
    print("Test Passed")
else:
    print("Test Failed")

# Further output is made to allow for manual testing.

print("\nNewton's Method\n")

print("sqrt(2) = " + str(q8.newton_sqrt(2)))
print("sqrt(3) = " + str(q8.newton_sqrt(3)))
print("sqrt(4) = " + str(q8.newton_sqrt(4)))
print("sqrt(5) = " + str(q8.newton_sqrt(5)))
print("sqrt(6) = " + str(q8.newton_sqrt(6)))
print("sqrt(7) = " + str(q8.newton_sqrt(7)))
print("sqrt(8) = " + str(q8.newton_sqrt(8)))
print("sqrt(9) = " + str(q8.newton_sqrt(9)))
print("sqrt(10) = " + str(q8.newton_sqrt(10)))

print("\nHalley's Method\n")

print("sqrt(2) = " + str(q8.halley_sqrt(2)))
print("sqrt(3) = " + str(q8.halley_sqrt(3)))
print("sqrt(4) = " + str(q8.halley_sqrt(4)))
print("sqrt(5) = " + str(q8.halley_sqrt(5)))
print("sqrt(6) = " + str(q8.halley_sqrt(6)))
print("sqrt(7) = " + str(q8.halley_sqrt(7)))
print("sqrt(8) = " + str(q8.halley_sqrt(8)))
print("sqrt(9) = " + str(q8.halley_sqrt(9)))
print("sqrt(10) = " + str(q8.halley_sqrt(10)))
