import sys

math_functions = {}

def plus(o1, o2):
    return o1 + o2
def minus(o1, o2):
    return o1 - o2
def times(o1, o2):
    return o1 * o2
def divide(o1, o2):
    return o1/o2

math_functions['+'] = plus
math_functions['-'] = minus
math_functions['*'] = times
math_functions['/'] = divide

def get_expression(operand1, operand2, operator):
    fallback = "({0} {1} {2})".format(operand1, operator, operand2)
    if operand1[-1].isdigit() and operand2[-1].isdigit():
        operand1 = float(operand1)
        operand2 = float(operand2)
        result = math_functions[operator](operand1, operand2)
        return str(result)

    if operand1 == operand2:
        if operator == '+':
            return "(2*" + operand1 + ")"
        elif operator == '-':
            return '0'
        elif operator == '/':
            return '1'

    if operand1 == '0':
        if operator == '*':
            return '0'
        elif operator == '+':
            return operand2

    return fallback

class Stack:
    def __init__(self):
        self.array = []

    def push(self, element):
        self.array.insert(0, element)

    def pop(self):
        element = self.array[0]
        self.array = self.array[1:]

        return element

    def peek(self):
        return self.array[0]

    def isEmpty(self):
        return len(self.array) == 0

    def __repr__(self):
        return str(self.array)


def get_inffix_formula(preffix):
    signs = preffix.split()

    operatorStack = Stack()
    operandStack = Stack()
    i = 0
    operandCnt = 0
    while True:
        if i == len(signs):
            break

        sign = signs[i]

        if sign[-1].isalnum():
            operandStack.push(sign)
            operandCnt += 1
            if operandCnt >= 2:
                operand2 = operandStack.pop()
                operand1 = operandStack.pop()
                operator = operatorStack.pop()
                expression = get_expression(operand1, operand2, operator)
                operandStack.push(expression)
                operandCnt -= 1

        else:
            operatorStack.push(sign)
            if operandCnt == 1:
                operandCnt = 0

        i = i + 1
    while not operatorStack.isEmpty():
        operand2 = operandStack.pop()
        operand1 = operandStack.pop()
        operator = operatorStack.pop()
        expression = get_expression(operand1, operand2, operator)
        operandStack.push(expression)

    result = operandStack.pop()
    return result

if __name__ == '__main__':
    preffix = sys.argv[1]
    result = get_inffix_formula(preffix)
    print(result)
