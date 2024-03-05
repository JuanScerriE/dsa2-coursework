import answers.q5 as q5

# Some test RPN expressions are intput into the lexer and
# evaluated to check that the algorithm is parsing correctly and
# that its output is accurate.

print("RPN Calculator Tests")

if 7.875 == q5.evaluate(q5.lex("65 32 -     7 32.125 - +")):
    print("\nTest Passed\n")
else:
    print("\nTest Failed\n")

if -82.7860696517413 == q5.evaluate(q5.lex("65 32 *     7 32.125 - /")):
    print("\nTest Passed\n")
else:
    print("\nTest Failed\n")

if -829.125 == q5.evaluate(q5.lex("65 32 - 7 32.125 - *")):
    print("\nTest Passed\n")
else:
    print("\nTest Failed\n")

# Here a user can input any expression of his choice.

expr = input("Input RPN Expression: ")

print("Result: " + str(q5.evaluate(q5.lex(expr))))
