import answers.q11 as q11
import math

# The sine and cosine functions are called with a number of
# different values. The results are compared to the expected
# output up to 4 decimal places of accuracy.

print("`sin` Tests\n")

if 0.9986 == round(q11.sin(45.5), 4):
    print("Test Passed")
else:
    print("Test Failed")

if -0.9869 == round(q11.sin(23.4), 4):
    print("Test Passed")
else:
    print("Test Failed")


print("\n`cos` Tests\n")

if 0.9994 == round(q11.cos(88), 4):
    print("Test Passed")
else:
    print("Test Failed")

if 0.8439 == round(q11.cos(12), 4):
    print("Test Passed")
else:
    print("Test Failed")

# Further printing is being done to allow for manual testing.

print("\nSine Output (In Radians)\n")

print("sin(45) = " + str(q11.sin(45)))
print("sin(12) = " + str(q11.sin(12)))
print("sin(0.5) = " + str(q11.sin(0.5)))
print("sin(0) = " + str(q11.sin(0)))

print("\nCosine Output (In Radians)\n")

print("cos(-13) = " + str(q11.cos(-13)))
print("cos(pi) = " + str(q11.cos(math.pi)))
print("cos(1.2345) = " + str(q11.cos(1.2345)))
print("cos(45) = " + str(q11.cos(45)))
