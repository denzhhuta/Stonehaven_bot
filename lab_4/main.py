from List import Stack
from List import Queue 

def main():
    queue = Queue()
    stack = Stack()
    while True:
        print("1. Додати елемент в стек")
        print("2. Видалити елемент зі стеку")
        print("3. Показати вміст стеку")
        print("4. Додати елемент в чергу")
        print("5. Видалити елемент з черги")
        print("6. Показати вміст черги")
        print("7. Вийти з програми")
        choice = int(input("Виберіть дію: "))
        if choice == 1:
            data = input("Введіть дані для додавання: ")
            stack.push(data)
            stack.show()
        elif choice == 2:
            popped_element = stack.pop()
            if popped_element is None:
                print("Стек порожній")
            else:
                print("Видалено: ", popped_element)
                stack.show()
        elif choice == 3:
            stack.show()
        elif choice == 4:
            data = input("Введіть дані для додавання: ")
            queue.enqueue(data)
            queue.display()
        elif choice == 5:
            popped_element = queue.dequeue()
            if popped_element is None:
                print("Черга порожня")
            else:
                print("Видалено: ", popped_element)
                queue.display()
        elif choice == 6:
            queue.display()
        elif choice == 7:
            break
        else:
            print("Невірний вибір")


if __name__ == '__main__':
    main()