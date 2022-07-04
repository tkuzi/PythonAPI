# deze imlementatie van een hash table is niet efficient en dient enkel voor de data structuur
class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node

class Data:
    def __init__(self,key,value) -> None:
        self.key = key
        self.value = value

class Hash_Table:
    def __init__(self,table_size) -> None:
        self.table_size = table_size
        self.hash_table = [None] * table_size #attribute omdat dit niet met argument wordt gegeven
        #[None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]

    def custom_hash(self,key):
        hash_value = 0
        for i in key:
            hash_value += ord(i) #ord is een functie om een key naar unicode integere om te zetten -> "hi" wordt dan een getal en dan is sneller te vinden
            hash_value = (hash_value * ord(i)) % self.table_size #randomness toevoegen omdat er anders 2 keys dezelfde hash_value kunnen hebben 
            #// zorgt er ook voor dat de hashvalue niet meer kan zijn als de tablesize dankzij de remainder 
        return hash_value

    def add_key_value(self,key,value):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is None:
            self.hash_table[hashed_key] = Node(Data(key,value),None)
        else:
            node = self.hash_table[hashed_key]
            while node.next_node: 
                node = node.next_node
            node.next_node = Node(Data(key,value),None)

    def get_value(self,key):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] is not None:
            node = self.hash_table[hashed_key]
            if node.next_node is None:
                return node.data.value
            while node.next_node:
                if key == node.data.key:
                    return node.data.value
                node = node.next_node
            if key == node.data.key:
                return node.data.value
        return None

    def print_table(self):
        print("{")
        for i,val in enumerate(self.hash_table):

            if val is not None:
                linked_list = ""
                node = val
                if node.next_node:
                    while node.next_node:
                        linked_list += (str(node.data.key) + " : " + str(node.data.value) + " --> ")
                        node = node.next_node

                    linked_list += (str(node.data.key) + " : " + str(node.data.value) + " --> None")
                    print(f"  [{i}]  {linked_list}")
                else:
                    linked_list += (str(node.data.key) + " : " + str(node.data.value) + " --> None")
                    print(f"  [{i}]  {linked_list}")
            else: 
                print(f" [{i}] {val}")
        print("}")



# ht = HashTable(4)
# ht.add_key_value("hi","value")
# ht.add_key_value("Thoams","value")
# ht.add_key_value("Siemnes","value")
# ht.add_key_value("POPO","value")
# ht.print_table()
