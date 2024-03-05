import answers.q6 as q6

# A list of known primes is embedded in script to allow for
# testing of the sieve and the primality test. Again comparisons
# to the expected result are made.

known_primes = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
    127,
    131,
    137,
    139,
    149,
]

print("Primality Tests")

if q6.is_prime(known_primes[5]) == True:
    print("Test Passed")
else:
    print("Test Failed")

if q6.is_prime(known_primes[10]) == True:
    print("Test Passed")
else:
    print("Test Failed")

if q6.is_prime(known_primes[23]) == True:
    print("Test Passed")
else:
    print("Test Failed")


print("\nSieve Test")

generated_primes = q6.f_sieve(150)

test_pass = True

for i in range(len(generated_primes)):
    if generated_primes[i] != known_primes[i]:
        test_pass = False

if test_pass:
    print("Test Passed")
else:
    print("Test Failed")
