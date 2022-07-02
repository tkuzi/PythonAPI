class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node 

#keep track of the lenght of our linked list
class LinkedList:
    def __init__(self):
        self.head = None
        self.last_node = None

    def print_LL(self):
        ll_string = ""
        node = self.head
        if node is None:
            print(None)
        while node:
            ll_string += f" {str(node.data)} ->"
            node = node.next_node
        
        ll_string += " None"
        print(ll_string)


ll = LinkedList()
node4 = Node("data4",None)
node3 = Node("data3",node4)
node2 = Node("data2",node3)
node1 = Node("data1",node2)

ll.head = node1
ll.print_LL()