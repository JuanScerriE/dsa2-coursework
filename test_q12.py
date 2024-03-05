import answers.q12 as q12

# An array of generated Fibonacci sums is tested against the
# expected array of Fibonacci sums.

print("Fibonacci Test")

if [1, 2, 4, 7, 12, 20, 33, 54, 88] == [q12.sum_fib(k) for k in range(1, 10)]:
    print("\nTest Passed\n")
else:
    print("\nTest Failed\n")

print("Sequence of Fibonacci Sums:\n")

for k in range(1, 20):
    print(q12.sum_fib(k), end=" ")

print()
