class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None
        
class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        
    def is_empty(self):
        return self.head is None
    
    def add_begin(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
    
    def add_end(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            
    def del_begin(self):
        if self.is_empty():
            return
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.head = self.head.next
            self.head.prev = None
    
    def del_end(self):
        if self.is_empty():
            return
        if self.head == self.tail:
            self.head = None
            self.tail = None
        else:
            self.tail = self.tail.prev
            self.tail.next = None
            
    def search(self, key):
        curr_node = self.head
        while curr_node is not None:
            if curr_node.data == key:
                return curr_node
            curr_node = curr_node.next
        return None
    
    def add_mid(self, key, data):
        curr_node = self.search(key)
        if curr_node is None:
            return
        new_node = Node(data)
        new_node.next = curr_node.next
        new_node.prev = curr_node
        if curr_node.next is not None:
            curr_node.next.prev = new_node
        curr_node.next = new_node
        
    def del_mid(self, key):
        curr_node = self.search(key)
        if curr_node is None:
            return
        if curr_node == self.head:
            self.del_begin()
        elif curr_node == self.tail:
            self.del_end()
        else:
            curr_node.prev.next = curr_node.next
            curr_node.next.prev = curr_node.prev
            
    def display(self):
        curr_node = self.head
        while curr_node is not None:
            print(curr_node.data, end=' ')
            curr_node = curr_node.next
        print()
