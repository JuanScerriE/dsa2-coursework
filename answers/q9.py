# This algorithm makes use of the properties of the builtin
# Python dictionary type (which is constructed off of a hash
# table).
#
# The idea: All the elements of an array are looped over once
# indexing every element in the dictionary.
#
# If the dictionary already contains the element, the algorithm
# will increase the count, otherwise it will add the new element
# to the dictionary. This means that the list was looped over
# once to count how many times each unique element occurs.
#
# During the process a dictionary is being populated. The worst
# case space-complexity is O(n). Moreover, the average case
# time-complexity of the dictionary is O(1).
#
# This means that this algorithm has an average time-complexity
# of O(2n) ( = O(n) ) since the algorithm loops over each
# element twice: once to index the elements in the dictionary
# and the other time to check which ones have duplicates.
#
# Moreover, the space-complexity of our algorithm is also O(2n)
# since we are creating a second array to hold all the values
# which have duplicates, in addition to the space-complexity of
# the dictionary.
#
# Note: The above is only discussing the average case
# time-complexity. The worst case time-complexity is O(n^2).
# However, this is very unlikely.


def find_dups(list):
    dict = {}

    for i in range(len(list)):
        if dict.get(list[i], 0) == 0:
            dict[list[i]] = 1
        else:
            dict[list[i]] += 1

    dups = []

    for key in dict:
        if dict[key] != 1:
            dups.append(key)

    return dups
