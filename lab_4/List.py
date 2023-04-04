class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

# class Queue:
#     def __init__(self):
#         self.data = []

#     def is_empty(self):
#         return len(self.data) == 0

#     def enqueue(self, data):
#         self.data.append(data)

#     def dequeue(self):
#         if self.is_empty():
#             return None
#         return self.data.pop(0)

#     def display(self):
#         print(self.data)

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def is_empty(self):
        return self.head is None

    def enqueue(self, data):
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        if self.is_empty():
            return None
        popped_node = self.head
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        popped_node.next = None
        return popped_node.data

    def display(self):
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next
        print()


class Stack:
    def __init__(self):
        self.head = None

    def push(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.head is None:
            return None
        popped_node = self.head
        self.head = self.head.next
        popped_node.next = None
        return popped_node.data

    def show(self):
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next
        print()

 #v2
# class Stack:
#     def __init__(self):
#         self.stack = []

#     def push(self, data):
#         self.stack.insert(0, data)

#     def pop(self):
#         if not self.is_empty():
#             return self.stack.pop()

#     def is_empty(self):
#         return len(self.stack) == 0

#     def show(self):
#         print(self.stack)
