class Node:
    def __init__(self, data = None, next_node = None):
        self.data = data
        self.next_node = next_node

class LinkedList:
    def __init__(self):
        self.head = None
        self.last_node = None
#return array with all the node data
    def to_list(self):
        l = []
        if self.head is None:
            return l
        node = self.head
        while node:
            l.append(node.data)
            node = node.next_node
        print("array",l)
        return l


    def print_ll(self):
        ll_string = ""
        node = self.head
        if node is None:
            print("None")
        while node:
            ll_string += f"{str(node.data)} ->"
            node = node.next_node
        
        ll_string += ' None'
        print(ll_string)

    def insert_start(self, data):

        if self.head is None:
            self.head = Node(data,None)
            self.last_node = self.head
        new_node = Node(data,self.head) # de link is de huidige head
        self.head = new_node

    def insert_end(self ,data):
        if self.head is None:
            self.insert_start(data)
         
        self.last_node.next_node = Node(data,None)
        self.last_node = self.last_node.next_node