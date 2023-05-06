def bit_depth_increase(number_bin, bit, size=32):  # Возвращает 32-битное число
    while len(number_bin) < size:
        number_bin.insert(1, bit)
    return number_bin


def right_shift(bin, shift):
    for _ in range(shift):
        bin.insert(0, 0)
        bin.pop()


def to_binary(_num, size=32):
    num = _num
    result = []
    is_positive = num >= 0
    num = abs(num)

    while num > 0:
        result.append(num % 2)
        num //= 2

    if len(result) <= 32:
        result.reverse()
        if is_positive:
            result.insert(0, 0)
        else:
            result.insert(0, 1)
        result = bit_depth_increase(result, bit=0, size=size)
        return result
    else:
        pass  # Переполнение


def reverse_bin(number_bin):  # Возвращает инверсию полученного двоичного числа, бит под знак остаётся
    result = []
    for i in range(1, len(number_bin)):
        result.append(1 - number_bin[i])
    result.insert(0, number_bin[0])
    return result


def sum_binary(_number1_bin, _number2_bin):  # Возвращает двоичное число
    overflow = 0
    result = []

    _number1_bin.reverse()
    _number2_bin.reverse()
    for obj in zip(_number1_bin, _number2_bin):
        value = obj[0] + obj[1] + overflow
        overflow = value // 2
        result.append(value % 2)
    _number1_bin.reverse()
    _number2_bin.reverse()

    result.reverse()
    if len(result) <= 32:
        return result
    else:
        pass  # переполнение


def to_int(_number_bin):
    num = _number_bin
    result = 0

    num.reverse()
    for i in range(0, len(num) - 1):
        result += (2 ** i) * num[i]
    num.reverse()

    if num[0] == 1:
        result = -result

    return result
