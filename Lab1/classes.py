from functions import *


class Number:
    int_form = 0
    straight_form = [4 for _ in range(32)]
    reverse_form = [2 for _ in range(32)]
    addiction_form = [3 for _ in range(32)]
    remainder = ""

    def __init__(self, _num=0, _bin=None, _str=""):
        self.remainder = _str
        if _num != 0:
            self.int_form = _num
            self.straight_form = to_binary(self.int_form)
        elif _bin is not None:
            self.straight_form = _bin
            self.straight_form = bit_depth_increase(self.straight_form, bit=0)
            self.int_form = to_int(_bin)

        if self.int_form < 0:
            self.reverse_form = reverse_bin(self.straight_form)
            binary_1 = bit_depth_increase([0, 1], bit=0)
            self.addiction_form = sum_binary(self.reverse_form, binary_1)
        else:
            self.reverse_form = self.straight_form
            self.addiction_form = self.straight_form

    def __add__(self, other):
        if self.straight_form[0] == other.straight_form[0]:
            binary_answer = sum_binary(self.straight_form, other.straight_form)
        else:
            binary_answer = sum_binary(self.addiction_form, other.addiction_form)
            if binary_answer[0] == 1:
                binary_answer = reverse_bin(binary_answer)
                binary_1 = bit_depth_increase([0, 1], bit=0)
                binary_answer = sum_binary(binary_answer, binary_1)

        result = Number(_num=0, _bin=binary_answer)
        return result

    def __mul__(self, other):
        list_of_terms = []
        is_ans_positive = self.straight_form[0] == other.straight_form[0]
        f_operand = list(self.straight_form)
        s_operand = list(other.straight_form)

        f_operand.pop(0)
        s_operand.pop(0)
        s_operand.reverse()

        for bit in s_operand:
            if bit == 1:
                temp = list(f_operand)
                list_of_terms.append(temp)
            else:
                temp = [0 for _ in range(31)]
                list_of_terms.append(temp)

        for i in range(1, len(list_of_terms)):
            for _ in range(i):
                list_of_terms[i].append(0)
                list_of_terms[i].pop(0)
            list_of_terms[0] = sum_binary(list_of_terms[0], list_of_terms[i])

        if is_ans_positive:
            list_of_terms[0].insert(0, 0)
        else:
            list_of_terms[0].insert(0, 1)

        result = Number(_num=0, _bin=list_of_terms[0])
        return result

    def __truediv__(self, other):
        is_ans_positive = self.straight_form[0] == other.straight_form[0]
        f_operand = list(self.straight_form)
        s_operand = list(other.straight_form)
        f_operand.pop(0)
        s_operand.pop(0)
        remainder = []
        result = []
        for i in range(len(f_operand)):
            remainder.append(f_operand[i])
            if to_int(remainder) >= to_int(s_operand):
                subtrahend = list(s_operand)
                subtrahend[0] = 1 - subtrahend[0]
                subtrahend = reverse_bin(subtrahend)
                subtrahend = sum_binary(subtrahend, bit_depth_increase(number_bin=[0, 1], bit=0))
                remainder = sum_binary(remainder, subtrahend)
                result.append(1)
            else:
                result.append(0)

        result_remainder = "."
        if 1 in remainder:
            for _ in range(5):
                remainder.append(0)
                if to_int(remainder) >= to_int(s_operand):
                    subtrahend = list(s_operand)
                    subtrahend[0] = 1 - subtrahend[0]
                    subtrahend = reverse_bin(subtrahend)
                    subtrahend = sum_binary(subtrahend, bit_depth_increase(number_bin=[0, 1], bit=0))
                    remainder = sum_binary(remainder, subtrahend)
                    result_remainder += "1"
                else:
                    result_remainder += "0"

        if is_ans_positive:
            result.insert(0, 0)
        else:
            result.insert(0, 1)

        result_number = Number(_bin=result, _str=result_remainder)
        return result_number

    def show(self):
        print(self.int_form)
        print("Прямой код:", *self.straight_form, self.remainder, sep='')
        print("Обратный код:", *self.reverse_form, sep='')
        print("Дополнительный код:", *self.addiction_form, sep='')
        print('-' * 50)


class FloatingPointNumber:
    sign = [0]
    exp = [0 for _ in range(8)]
    mantissa = [0 for _ in range(23)]
    float_form = 0.0

    def __init__(self, _num=0, _sign=None, _exp=None, _mantissa=None):
        if _num != 0:
            self.float_form = _num
            self.to_floating_point_binary()

        elif _exp is not None and _mantissa is not None:
            self.float_form = _num
            self.exp = _exp
            self.mantissa = _mantissa
            self.sign = _sign
            # self.to_float()

    def to_floating_point_binary(self):
        exponent = []
        exp = 0
        sign = [1] if self.float_form < 0 else [0]
        for i in range(-127, 255):
            if abs(self.float_form) < 2 ** i:
                exp = i - 1
                exponent = to_binary(i - 1 + 127, size=8)
                if len(exponent) > 8:
                    exponent.pop(0)
                break

        self.sign = sign
        self.exp = exponent
        self.get_mantissa(exp)

    def get_mantissa(self, max_exponent):
        mantissa = []
        start = max_exponent
        float1 = abs(self.float_form)
        for i in range(start, start - 24, -1):
            if float1 >= 2 ** i:
                float1 -= 2 ** i
                mantissa.append(1)
            else:
                mantissa.append(0)

        mantissa.pop(0)
        self.mantissa = mantissa

    def to_float(self):
        mant = list(self.mantissa)
        exp = list(self.exp)

        exp_int = 0
        for i in range(len(exp)):
            exp_int += (2 ** (len(exp) - 1 - i)) * exp[i]
        exp_int -= 127
        result = 2 ** (exp_int + 1)
        for i in range(0, len(mant)):
            result += (2 ** (exp_int - 1 - i)) * mant[i]

        self.float_form = result

    def show(self):
        print(self.float_form)
        print("Порядок: ", *self.exp, sep='')
        print("Мантисса: ", *self.mantissa, sep='')
        print('-' * 50)

    def __add__(self, other):
        f_exp = list(self.exp)
        s_exp = list(other.exp)
        f_mant = list(self.mantissa)
        s_mant = list(other.mantissa)
        f_exp.insert(0, 0)
        s_exp.insert(0, 1)
        f_mant.insert(0, 1)
        s_mant.insert(0, 1)

        s_exp = reverse_bin(s_exp)
        binary_1 = bit_depth_increase([0, 1], 0, 9)
        s_exp = sum_binary(s_exp, binary_1)
        shift_bin = sum_binary(f_exp, s_exp)
        if shift_bin[0] == 1:
            shift_bin = reverse_bin(shift_bin)
            shift_bin = sum_binary(shift_bin, binary_1)
        shift = to_int(shift_bin)

        result_exp = list(f_exp)
        if shift > 0:
            result_exp = list(f_exp)
            right_shift(s_mant, shift)
        elif shift < 0:
            result_exp = list(s_exp)
            right_shift(f_mant, -shift)
        r_mant = sum_binary(f_mant, s_mant)
        r_mant.pop(0)
        result_exp.pop(0)
        result_float = self.float_form + other.float_form
        result = FloatingPointNumber(_num=result_float, _exp=result_exp, _mantissa=r_mant)
        return result
