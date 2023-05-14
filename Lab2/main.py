from prettytable import PrettyTable


def check_syntax(_input):
    stack = []
    for item, next_item in zip(_input, _input[1:] + ' '):
        if item == '(':
            stack.append('(')
        elif stack and item == ')':
            stack.pop()
        elif not stack and item == ')':
            return False
        elif item.isdigit() and not 1 <= int(item) <= 3:
            return False
        elif item.isalpha() and item != 'x':
            return False
        elif item.isalpha() and next_item.isalpha():
            return False

    return not stack


def get_index(answers):
    result = 0

    for i in range(8):
        if answers[i]:
            result += 2 ** (len(answers) - 1 - i)

    return result


def sdnf(combines, answers, variables=["x1", "x2", "x3"]):
    sdnf_binary = ""
    Sdnf = ""
    Sdnf_dec = []
    for i in range(8):
        if answers[i]:
            Sdnf_dec.append(str(i))
            for j in range(3):
                if combines[i][j] == 1:
                    Sdnf += variables[j]
                else:
                    Sdnf += ('-' + variables[j])
                Sdnf += ' * '
            Sdnf = Sdnf[:-3]
            Sdnf += ' + '
    Sdnf = Sdnf[:-3]

    for i in range(8):
        if answers[i]:
            for item in combines[i]:
                sdnf_binary += str(item)
            sdnf_binary += '+'
    sdnf_binary = sdnf_binary[:-1]

    return Sdnf, sdnf_binary, Sdnf_dec


def sknf(combines, answers, variables=["x1", "x2", "x3"]):
    Sknf = ""
    Sknf_binary = ""
    Sknf_dec = []
    for i in range(8):
        if not answers[i]:
            Sknf_dec.append(str(i))
            Sknf += '('
            for j in range(3):
                if combines[i][j] == 0:
                    Sknf += variables[j]
                else:
                    Sknf += ('-' + variables[j])
                Sknf += ' + '
            Sknf = Sknf[:-3] + ')'
            Sknf += ' * '
    Sknf = Sknf[:-3]

    for i in range(8):
        if not answers[i]:
            for item in combines[i]:
                Sknf_binary += str(item)
            Sknf_binary += '*'
    Sknf_binary = Sknf_binary[:-1]

    return Sknf, Sknf_binary, Sknf_dec


def to_poland_postfix(_input):
    formula = list(_input)
    priorities = {
        '(': 0,
        '+': 1,
        '*': 2,
        '-': 3}
    operands = []
    answer = []
    for i in range(len(formula)):
        if formula[i] == 'x':
            answer.append(formula[i] + formula[i + 1])
            continue

        elif formula[i] == '(':
            operands.append(formula[i])

        elif formula[i] == ')':
            while operands[-1] != '(':
                answer.append(operands.pop())
            operands.pop()

        elif formula[i] in ['+', '*', '-']:
            while operands and priorities[operands[-1]] > priorities[formula[i]]:
                answer.append(operands.pop())
            operands.append(formula[i])

    answer += reversed(operands)
    return answer


def func_solution(_combine, _postfix_form):
    _answers = [item == 1 for item in _combine]
    stack = []
    for item in _postfix_form:
        if item[0] == 'x':
            ind = int(item[1]) - 1
            stack.append(_answers[ind])

        elif item == '*':
            f_oper = stack.pop()
            s_oper = stack.pop()
            res = f_oper and s_oper
            stack.append(res)

        elif item == '+':
            f_oper = stack.pop()
            s_oper = stack.pop()
            res = f_oper or s_oper
            stack.append(res)

        elif item == '-':
            f_oper = stack.pop()
            res = not f_oper
            stack.append(res)

    return stack[0]


def menu():
    table_data_output = []
    table_data_input = [
        [0, 0, 0],
        [0, 0, 1],
        [0, 1, 0],
        [0, 1, 1],
        [1, 0, 0],
        [1, 0, 1],
        [1, 1, 0],
        [1, 1, 1]
    ]
    print('"*" - конъюнкция, "+" - дизъюнкция, "-" - отрицание')
    formula = input("Введите булевую функцию f(x1, x2, x3): ")

    formula = formula.replace(' ', '')
    formula = formula.lower()
    try:
        assert check_syntax(formula)
    except AssertionError:
        print("Ошибка ввода")
        return
    postfix_form = to_poland_postfix(formula)
    for combine in table_data_input:
        item = func_solution(combine, postfix_form)
        table_data_output.append(item)

    table = PrettyTable()
    table.field_names = ["X1", "X2", "X3", "f(X1, X2, X3)"]
    for i in range(len(table_data_output)):
        table.add_row([table_data_input[i][0], table_data_input[i][1], table_data_input[i][2], 1 if table_data_output[i] else 0])
    print("Таблица истинности:")
    print(table)
    Sdnf, Sdnf_binary, Sdnf_decimal = sdnf(table_data_input, table_data_output)
    Sknf, Sknf_binary, Sknf_decimal = sknf(table_data_input, table_data_output)
    index = get_index(table_data_output)
    print("СДНФ:", Sdnf, Sdnf_binary + '= V(' + ",".join(Sdnf_decimal) + ')', '-' * 30, sep='\n')
    print("СКНФ:", Sknf, Sknf_binary + '= ^(' + ",".join(Sknf_decimal) + ')', '-' * 30, sep='\n')
    print("ИНДЕКС:", index)


menu()
