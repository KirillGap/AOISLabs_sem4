class Processor:
    def __init__(self, decimal_digits):
        self.table = []
        self.decimal_digits = decimal_digits
        self.g_trigger, self.l_trigger = False, False
        self.to_bin_form()

    def __str__(self):
        str_form = ''
        for line in self.table:
            str_form += f'{line}\n'
        return str_form

    def to_bin_form(self):
        for digit in self.decimal_digits:
            temp_bin_num = []
            while digit:
                temp_bin_num.append(digit % 2)
                digit //= 2
            temp_bin_num.reverse()
            while len(temp_bin_num) < 8:
                temp_bin_num.insert(0, 0)
            self.table.append(temp_bin_num)

    def update_triggers(self, a, S):
        g, l = self.g_trigger, self.l_trigger
        self.g_trigger = g or (not a and S and not l)
        self.l_trigger = l or (a and not S and not g)

    def find_by_interval(self, min_bin, max_bin):
        result = []
        for binary_num in self.table:
            self.g_trigger, self.l_trigger = False, False
            temp_flag = True
            for index, value in enumerate(binary_num):
                self.update_triggers(bool(min_bin[index]), bool(value))
            if not self.g_trigger and self.l_trigger:
                temp_flag = False
            self.l_trigger, self.g_trigger = False, False
            for index, value in enumerate(binary_num):
                self.update_triggers(bool(max_bin[index]), bool(value))
            if self.g_trigger and not self.l_trigger:
                temp_flag = False

            if temp_flag:
                result.append(binary_num)
        return result

    def find_by_mask(self, mask):
        result = []
        for binary_num in self.table:
            flag = True
            for mask_bit, num_bit in zip(mask, binary_num):
                if not (mask_bit == '_' or (int(mask_bit) and num_bit) or (not int(mask_bit) and not num_bit)):
                    flag = False
                    break
            if flag:
                result.append(binary_num)
        return result