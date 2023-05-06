import classes


def menu():
    while True:
        print("0) Выход")
        print("1) Сумма целых чисел")
        print("2) Произведение целых чисел")
        print("3) Частное целых чисел")
        print("4) Сумма чисел с плавающей точкой")
        command = int(input("Выберите задание: "))
        if command == 1 or command == 2 or command == 3:
            first_num = classes.Number(int(input("Введите первое число: ")))
            second_num = classes.Number(int(input("Введите второе число: ")))
            answer = classes.Number()
            if command == 1:
                answer = first_num + second_num
            elif command == 2:
                answer = first_num * second_num
            elif command == 3:
                answer = first_num / second_num
            first_num.show()
            second_num.show()
            answer.show()
        elif command == 4:
            first_num = classes.FloatingPointNumber(float(input("Введите первое число: ")))
            second_num = classes.FloatingPointNumber(float(input("Введите второе число: ")))
            first_num.show()
            second_num.show()
            answer = first_num + second_num
            answer.show()
        elif command == 0:
            break
        else:
            print("Ошибка")


menu()
