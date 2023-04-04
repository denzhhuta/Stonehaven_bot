class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
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
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def del_begin(self):
        if self.is_empty():
            return None
        popped_node = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        popped_node.next = None
        return popped_node.data

    def del_end(self):
        if self.is_empty():
            return None
        popped_node = self.tail
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        popped_node.prev = None
        return popped_node.data

    def search(self, key):
        current = self.head
        while current:
            if current.data == key:
                print("Found node:", current.data)
                return current
            current = current.next
        return None

    # def add_mid(self, data, key):
    #     key_node = self.search(key)
    #     if key_node is None:
    #         print("Key node not found")
    #         return False
    #     print("Inserting new node after:", key_node.data)
    #     new_node = Node(data)
    #     new_node.next = key_node.next
    #     new_node.prev = key_node
    #     if key_node.next is not None:
    #         key_node.next.prev = new_node
    #     key_node.next = new_node
    #     if key_node == self.tail:
    #         self.tail = new_node
    #     return True
    
    def add_mid(self, data, key):
        key_node = self.search(str(key))
        if key_node is None:
            return False
        new_node = Node(str(data))
        new_node.next = key_node.next
        new_node.prev = key_node
        if key_node.next is not None:
            key_node.next.prev = new_node
        key_node.next = new_node
        if key_node == self.tail:
            self.tail = new_node
        return True



    def del_mid(self, key):
        key_node = self.search(key)
        if key_node is None:
            return False
        if key_node.prev is None:
            self.head = key_node.next
        else:
            key_node.prev.next = key_node.next
        if key_node.next is None:
            self.tail = key_node.prev
        else:
            key_node.next.prev = key_node.prev
        key_node.next = None
        key_node.prev = None
        return True

    def display(self):
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next
        print()
