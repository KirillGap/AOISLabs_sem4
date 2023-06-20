class HashTable:

    class Element:
        def __init__(self, _key, _value):
            self.key, self.value = _key, _value

        def __str__(self):
            return f'[{self.key} : {self.value}]'

    def __init__(self, size=8, const=2):
        self.size = size
        self.count_of_empty_cells = self.size
        self.const = const
        self.table = [[] for _ in range(self.size)]

    def hash_func(self, _key):
        hash_value = 0
        for i, char in enumerate(_key):
            hash_value += (ord(char) << (i % self.const))
        return hash_value % self.size

    def insert(self, key, value):
        index = self.hash_func(key)
        elem = self.Element(key, value)
        if not self.table[index]:
            self.count_of_empty_cells -= 1
        if len(self.table[index]) <= 1:
            self.table[index].append(elem)
        else:
            self.print_collision(elem, self.table[index])
            self.rebase_table()
            self.insert(key, value)

    def find(self, key):
        result = []
        index = self.hash_func(key)
        for elem in self.table[index]:
            result.append(elem.value if elem.key == key else None)
        if result:
            return result
        else:
            return -1

    def remove(self, key):
        if self.remove_element(key):
            print(f'success! element with key: {key} deleted!')
        else:
            print(f'error! element with key: {key} not founded!')

    def remove_element(self, key):
        flag = False
        index = self.hash_func(key)
        for i, elem in enumerate(self.table[index]):
            if elem.key == key:
                self.table[index].pop(i)
                flag = True
        if flag and not self.table[index]:
            self.count_of_empty_cells += 1
        return flag

    def rebase_table(self):
        elems = []
        for line in self.table:
            if line:
                for item in line:
                    elems.append(item)
        self.size *= 2
        self.const *= 2
        self.__init__(size=self.size, const=self.const)
        for element in elems:
            self.insert(element.key, element.value)

    def __str__(self):
        str_form = ''
        for ID, line in enumerate(self.table):
            str_form += f'id[{ID}]: '
            if line:
                for item in line:
                    str_form += str(item)
            else:
                str_form += 'empty'
            str_form += ';\n'
        return str_form

    @staticmethod
    def print_collision(new_element, already_existing):
        print(f'collision! {new_element} -> [{already_existing[0]}, {already_existing[1]}]')
        print('hash table rebased')
