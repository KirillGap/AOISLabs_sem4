from Memory import Memory

def check_input(input: str) -> int:
    try:
        new_input = int(input)
        if not 0 <= new_input <= 15:
            raise ValueError
    except ValueError:
        print("Ошибка ввода", input, sep='  ')
        return False
    return True


if __name__ == '__main__':
    memory1 = Memory()
    print(memory1)

    index1, index2 = input('Выберите 2 слова для f1(введите индекс слова 0-15): '), input()
    while not(check_input(index1) and check_input(index2)):
        index1, index2 = input('Выберите 2 слова для f1(введите индекс слова 0-15): '), input()
    print(f'результат f1: {memory1.f1(int(index1), int(index2))}')

    index1 = input('Выберите слово для f3(введите индекс слова 0-15): ')
    while not check_input(index1):
        index1 = input('Выберите слово для f3(введите индекс слова 0-15): ')
    print(f'результат f3: {memory1.f3(int(index1))}')

    index1 = input('Выберите слово для f12(введите индекс слова 0-15): ')
    while not check_input(index1):
        index1 = input('Выберите слово для f12(введите индекс слова 0-15): ')
    print(f'результат f12: {memory1.f12(int(index1))}')

    index1, index2 = input('Выберите 2 слова для f14(введите индекс слова 0-15): '), input()
    while not (check_input(index1) and check_input(index2)):
        index1, index2 = input('Выберите 2 слова для f14(введите индекс слова 0-15): '), input()
    print(f'результат f14: {memory1.f14(int(index1), int(index2))}')

    search_word = input('Введите слово для поиска значения ближайшего сверху(снизу): ')
    try:
        search_word = [int(i) for i in search_word]
        search_result = memory1.search(search_word)
        print(f'Результат поиска по слову: {search_word}\n'
              f'Слово ближайшее сверху: {search_result[0]}\n'
              f'Слово ближайшее снизу: {search_result[1]}\n')
    except ValueError:
        print('Ошибка ввода')

    mask = input('Задайте V = 000-111\n')
    try:
        mask = [int(i) for i in mask]
        if len(mask) != 3 or not all(i in [0, 1] for i in mask):
            mask = None
        operation_result = memory1.operation(mask)
        print(f'Результат операции при V={mask if mask else [0, 0, 0]}:')
        for i in range(len(operation_result)):
            print(operation_result[i])
    except ValueError:
        print('Ошибка ввода')
