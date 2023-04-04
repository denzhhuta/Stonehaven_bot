from List1 import DoublyLinkedList

dll = DoublyLinkedList()

while True:
    print("1. Add at beginning")
    print("2. Add at end")
    print("3. Delete from beginning")
    print("4. Delete from end")
    print("5. Search")
    print("6. Add after a node")
    print("7. Delete a node")
    print("8. Display")
    print("9. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        data = input("Enter data to add at the beginning: ")
        dll.add_begin(data)
        dll.display()

    elif choice == 2:
        data = input("Enter data to add at the end: ")
        dll.add_end(data)
        dll.display()

    elif choice == 3:
        dll.del_begin()
        dll.display()

    elif choice == 4:
        dll.del_end()
        dll.display()

    elif choice == 5:
        key = input("Enter data to search: ")
        result = dll.search(key)
        if result:
            print("Data found in the list.")
        else:
            print("Data not found in the list.")

    elif choice == 6:
        key = input("Enter data after which to add: ")
        data = input("Enter data to add: ")
        result = dll.search(key)
        if result:
            dll.add_mid(key, data)
            dll.display()
        else:
            print("Data not found in the list.")

    elif choice == 7:
        key = input("Enter data to delete: ")
        result = dll.search(key)
        if result:
            dll.del_mid(key)
            dll.display()
        else:
            print("Data not found in the list.")

    elif choice == 8:
        dll.display()

    elif choice == 9:
        break

    else:
        print("Invalid choice. Please try again.")
