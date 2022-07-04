# de linkse node is altijd een kleinere waarde dan de rechtse

class Node:
    def __init__(self,data = None):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def _insert_recursive(self, value, node):
        if value < node.data:
            if node.left is None:
                node.left = Node(value)
            else:
                self._insert_recursive(value,node.left)
        elif value > node.data:
            if node.right is None:
                node.right = Node(value)
            else:
                self._insert_recursive(value, node.right)
        else:
            return # als de value gelijk is aan een bestaande node


    def insert(self,value):
        if self.root is None: # This means the upper tree node is empty and thus the tree doesn't excsits
            self.root = Node(value)
        else:
            self._insert_recursive(value, self.root)
