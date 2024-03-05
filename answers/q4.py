class ProductTriple:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.ab = a * b

    def product_equals(self, other):
        if self.a != other.a and self.b != other.b and self.ab == other.ab:
            return True
        else:
            return False

    def equals(self, other):
        if self.a == other.a and self.b == other.b and self.ab == other.ab:
            return True
        else:
            return False


def merge(a, b):
    i = 0
    j = 0

    c = []

    while i < len(a) or j < len(b):
        if j == len(b) or (i < len(a) and a[i] <= b[j]):
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1

    return c


def mergesort(a):
    mid = len(a) // 2

    if len(a) == 1:
        return a

    b = mergesort(a[:mid])
    c = mergesort(a[mid:])

    return merge(b, c)


def find_products(a):
    if len(a) == 0:
        return a

    # Sort the array so we can deal with duplicates easily.
    a = mergesort(a)

    # The maximum size of products is n * (n - 1) / 2 where n is
    # the number of unique elements in the array.
    products = []

    prev_outer = a[0]

    # We make sure to end one less since we do not need to check
    # the last one.

    # This loop is used to generate all the triples which we
    # need. Specifically, It allows us to generate triples
    # where, the last element is the product of the first two.
    # Moreover, we generate unique products. This takes into
    # account the commutativity of multiplication so we do not
    # have doubles. Moreover, the time-complexity of this is
    # O(n(n-1)/2). This is the exact amount of iterations. We
    # keep track of the previous elements to make sure that we
    # do not repeat elements. Both in the outer loop and the
    # inner loop.
    for i in range(len(a) - 1):
        if prev_outer < a[i] or i == 0:
            prev_inner = a[i]
            # We do not check the product of the previous
            # elements because they have already been accounted
            # for by previous iterations.
            for j in range(i + 1, len(a)):
                if prev_inner < a[j]:
                    products.append(ProductTriple(a[i], a[j]))
                    prev_inner = a[j]

        prev_outer = a[i]

    related = []

    # A simliar approach is used here. This allows us to yield
    # completely different elements without explicity checking
    # the individual components of the products.
    for i in range(len(products) - 1):
        for j in range(i + 1, len(products)):
            if products[i].product_equals(products[j]):
                related.append((products[i], products[j]))

    return related
