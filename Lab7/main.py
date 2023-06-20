from Processor import Processor
from random import randint


def split(string):
    while len(string) < 8:
        string = '0' + string
    return [int(i) for i in string]


def check_mask(string):
    return len(string) == 8


if __name__ == '__main__':
    digits = []
    for _ in range(8):
        digits.append(randint(0, 255))
    proc = Processor(digits)
    print(digits, proc, sep='\n')

    while True:
        command = input('''
1 - Поиск величин, заключенных в заданном интервале
2 - Поиск по заданной маске
*любой другой ввод* - Выход
''')
        match command:
            case '1':
                min_border = input('min border:')
                max_border = input('max border:')
                min_border, max_border = split(min_border), split(max_border)
                print(min_border, max_border, sep='\n')
                print(proc.find_by_interval(min_border, max_border))

            case '2':
                mask = input('Введите маску, вместо переменных используйте "_":')
                if check_mask(mask):
                    print(proc.find_by_mask(mask))

            case _:
                break


