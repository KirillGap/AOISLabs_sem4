from random import choice


class Memory:
    def __init__(self):
        self.size = 16
        self.normal_table = [[choice([0, 1]) for _ in range(self.size)] for _ in range(self.size)]
        self.diagonal_table = [[-1 for _ in range(self.size)] for _ in range(self.size)]
        self.to_diagonal_form()

    def __str__(self):
        str_form = 'normal form:\n'
        for line in self.normal_table:
            for bit in line:
                str_form += str(bit) + ' '
            str_form += '\n'
        lst = self.__foo()
        lst.sort()
        lst_str = [str(i) for i in lst]
        str_form += ' '.join(lst_str)
        str_form += '\n\ndiagonal form:\n'
        for line in self.diagonal_table:
            for bit in line:
                str_form += str(bit) + ' '
            str_form += '\n'
        return str_form

    def to_diagonal_form(self):
        for i in range(self.size):
            for j in range(self.size):
                self.diagonal_table[i][j] = self.normal_table[i - j][j]

    def get_column(self, word_index):
        column = []
        for i in range(word_index, self.size):
            column.append(self.diagonal_table[i][word_index])
        for i in range(word_index):
            column.append(self.diagonal_table[i][word_index])
        return column

    def f1(self, word_index1, word_index2):  # Конъюнкция
        word1 = self.get_column(word_index1)
        word2 = self.get_column(word_index2)
        result = [i and j for i, j in zip(word1, word2)]
        return result

    def f3(self, word_index):
        word = self.get_column(word_index)
        return word

    def f12(self, word_index):
        word = self.get_column(word_index)
        for i in range(self.size):
            word[i] += (-1) ** word[i]
        return word

    def f14(self, word_index1, word_index2):
        result = self.f1(word_index1, word_index2)
        for i in range(self.size):
            result[i] += (-1) ** result[i]
        return result

    def search(self, word):
        word = self.complete_word(word)
        upper_words = []
        lower_words = []

        for i in range(self.size):
            check_word = self.get_column(i)
            if self.comparison(word, check_word):
                upper_words.append(check_word)
            else:
                lower_words.append(check_word)

        if lower_words:
            max_lower_word = lower_words[0]
            for i in range(1, len(lower_words)):
                if self.comparison(max_lower_word, lower_words[i]):
                    max_lower_word = lower_words[i]
        else:
            max_lower_word = 'None'

        if upper_words:
            min_upper_word = upper_words[0]
            for i in range(1, len(upper_words)):
                if not self.comparison(min_upper_word, upper_words[i]):
                    min_upper_word = upper_words[i]
        else:
            min_upper_word = 'None'

        result = []
        if min_upper_word:
            result.append(min_upper_word)
        if max_lower_word:
            result.append(max_lower_word)
        return result

    @staticmethod
    def comparison(first_word, second_word):
        g_trigger, l_trigger = 0, 0
        prev_g_trigger, prev_l_trigger = 0, 0

        for i in range(len(first_word)):
            g_trigger = prev_g_trigger or (not first_word[i] and second_word[i] and not prev_l_trigger)
            l_trigger = prev_l_trigger or (first_word[i] and not second_word[i] and not prev_g_trigger)
            prev_g_trigger, prev_l_trigger = g_trigger, l_trigger

        return g_trigger

    @staticmethod
    def complete_word(word):
        while len(word) < 16:
            word.insert(0, 0)
        return word

    def __foo(self):
        dec_vect = []
        for i in range(self.size):
            word = self.get_column(i)
            word.reverse()
            dec_form = 0
            for index, bit in enumerate(word):
                dec_form += bit * (2 ** index)
            dec_vect.append(dec_form)
        return dec_vect

    def operation(self, mask=None):
        if mask is None or len(mask) != 3:
            mask = [0, 0, 0]
        good_words = self.mask_search(mask)
        result = []
        for word in good_words:
            new_word = self.add(word)
            print(' '.join(str(i) for i in new_word))
            result.append(new_word)
        return result

    def add(self, word):
        A = word[3:7]
        B = word[7:11]
        A.reverse()
        B.reverse()
        S, carry = [], 0
        for bit1, bit2 in zip(A, B):
            new_bit, carry = (bit1 + bit2 + carry) % 2, (bit1 + bit2 + carry) // 2
            S.append(new_bit)
        S.append(carry)
        S.reverse()
        return word[:11] + S

    def mask_search(self, mask=None):
        good_words = []
        for i in range(self.size):
            word = self.get_column(i)
            if word[:3] == mask:
                good_words.append(word)
        return good_words
