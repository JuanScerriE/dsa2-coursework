from enum import Enum


class Branch(Enum):
    Left = 0
    Root = 1
    Right = 2


# The Node class is a class which holds a value and two pointers
# which will be populated with addresses to similar Node objects
# creating a tree structure.


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def add(self, node):
        if node.value > self.value:
            if self.right == None:
                self.right = node
            else:
                self.right.add(node)
        else:
            if self.left == None:
                self.left = node
            else:
                self.left.add(node)

    # The draw method is an inorder traversal of the BST.
    # Specifically, the right sub-tree will be printed first, then the
    # root and lastly the left sub-tree.
    #
    # The draw method has two parameters, s and parent. s is the
    # string which will be printed before the actual value is
    # printed. parent is an enum which allows us to keep track
    # of where our traverser is coming from. This allows us to
    # modify the string s accordingly to draw a tree.

    def draw(self, s, parent):
        if self.right != None:
            if parent == Branch.Right or parent == Branch.Root:
                self.right.draw(
                    s[: (len(s) - 1)] + " " + " " * len(str(self.value)) + " |",
                    Branch.Right,
                )
                print(s[: (len(s) - 1)] + " " + " " * len(str(self.value)) + "/")
            else:
                self.right.draw(
                    s[: (len(s) - 1)] + "|" + " " * len(str(self.value)) + " |",
                    Branch.Right,
                )
                print(s[: (len(s) - 1)] + "\\" + " " * len(str(self.value)) + "/")

        print(s[: (len(s) - 1)] + " " + str(self.value))

        if self.left != None:
            if parent == Branch.Left or parent == Branch.Root:
                print(s[: (len(s) - 1)] + " " + " " * len(str(self.value)) + "\\")
                self.left.draw(
                    s[: (len(s) - 1)] + " " + " " * len(str(self.value)) + " |",
                    Branch.Left,
                )
            else:
                print(s[: (len(s) - 1)] + "/" + " " * len(str(self.value)) + "\\")
                self.left.draw(
                    s[: (len(s) - 1)] + "|" + " " * len(str(self.value)) + " |",
                    Branch.Left,
                )
