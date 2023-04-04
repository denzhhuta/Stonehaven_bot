from List2 import LinkedList

def main():
    my_list = LinkedList()
    while True:
        print("\nDoubly Linked List Menu")
        print("1. Add element to beginning of list")
        print("2. Add element to end of list")
        print("3. Delete element from beginning of list")
        print("4. Delete element from end of list")
        print("5. Search for element in list")
        print("6. Add element to list after a specified element")
        print("7. Delete a specified element from list")
        print("8. Exit program")
        choice = int(input("Enter your choice: "))
        
        if choice == 1:
            data = input("Enter data for the new element: ")
            my_list.add_begin(data)
            my_list.display()
        elif choice == 2:
            data = input("Enter data for the new element: ")
            my_list.add_end(data)
            my_list.display()
        elif choice == 3:
            my_list.del_begin()
            my_list.display()
        elif choice == 4:
            my_list.del_end()
            my_list.display()
        elif choice == 5:
            key = input("Enter the key to search for: ")
            node = my_list.search(key)
            if node is None:
                print("Element not found")
            else:
                print("Element found")
        elif choice == 6:
            key = input("Enter the key after which to insert the new element: ")
            data = input("Enter data for the new element: ")
            my_list.add_mid(key, data)
            my_list.display()
        elif choice == 7:
            key = input("Enter the key of the element to delete: ")
            my_list.del_mid(key)
            my_list.display()
        elif choice == 8:
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == '__main__':
    main()