# python
# eval()
# from CS GUI calculator

# perform the calculation from the display
import debug_tools as debug

from MyLib import MStack, MQueue


def operate(operator, operand1, operand2):
    operand1, operand2 = float(operand1), float(operand2)
    if operator == '+':
        return operand1 + operand2
    if operator == '-':
        return operand1 - operand2
    if operator == '*':
        return operand1 * operand2
    if operator == '/':
        return operand1 / operand2


def list_to_number(digit_list):
    # convert a list of digits to an integer
    result = 0
    for digit in digit_list:
        result *= 10
        result += digit
    return result


def precedence(operator):
    PRECEDENCE = {
        '√': 1,
        '+': 2,
        '-': 2,
        '×': 3,
        '÷': 3,
        '^': 4,
        '(': 99999,
        # Not used for actually converting to prefix, used to test operators not missing
        ')': 99999,
    }
    return PRECEDENCE[operator]


class Node:
    OPERATOR = 1
    OPERAND = 2
    
    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return f'type: {self.type}, value: {self.value}'


class Calculator:
    # calculator class for calculating

    def __init__(self):
        # TODO:
        # - decide prefix or postfix -->> Using prefix, maybe postfix later
        # - implement infix to pre/post - fix
        # - implement basic operation with operator and 2 operands
        # - implement an set of functions to let the other file call
        # - create a python stub (pyi)

        # start stack with top at index 0

        self.__input_stack = MStack()
        self.__infix_equation = MQueue()
        self.__prefix_equation = MQueue()
        self.result = 0
        self.__infix = ''

    def __prepare_infix(self):
        operators = ['+', '-', '×', '÷', '√', '^', '(', ')']
        tmp = ''
        idx = 0
        while idx < len(self.__infix):
            if self.__infix[idx] in operators:
                if len(tmp) != 0:
                    self.__infix_equation.push(Node(Node.OPERAND, tmp))
                    tmp = ''
                self.__infix_equation.push(Node(Node.OPERATOR, self.__infix[idx]))
            else:
                tmp += self.__infix[idx]
            idx += 1
        if len(tmp) != 0:
            self.__infix_equation.push(Node(Node.OPERAND, tmp))

    def __infix_to_prefix(self):
        # convert infix into prefix
        '''
        for each item in MStack
            if is an operand:
                output
            else
                if stk is empty
                    push stk
                    continue
                if operator == (
                    push stk
                    continue
                if operator == )
                    while stk top not (
                        output
                    pop stk
                    continue
                if operator precedence <= stk top precedence
                    push stk
                    continue
                while operator precedence > stk top precedence
                    output
                else
                    push stk
        while stk is not empty
            output
        reverse result
        '''
        stk = MStack()

        for item in self.__infix_equation:
            if item.type == Node.OPERAND:
                self.__prefix_equation.push(item)
            else:
                if stk.empty():
                    stk.push(item)
                    continue
                if item.value == '(':
                    stk.push(item)
                    continue
                if item.value == ')':
                    while stk.top().value != '(':
                        self.__prefix_equation.push(stk.pop())
                    stk.pop()
                    continue
                if precedence(item.value) > precedence(stk.top().value):
                    stk.push(item)
                    continue
                while not stk.empty() and precedence(item.value) <= precedence(stk.top().value):
                    self.__prefix_equation.push(stk.pop())
                else:
                    stk.push(item)
        while not stk.empty():
            self.__prefix_equation.push(stk.pop())

        # reverse result
        self.__prefix_equation.lst = self.__prefix_equation.lst[::-1]

    def __calculate_prefix(self):
        '''
        for item in prefix equation
            if item is operator
                push into stack
            else
                while stack top is operand1
                    operand2 = pop stack
                    operator = pop stack
                    operate operand1 operator  operand2
                push result
        '''
        stk = MStack()
        for item in self.__prefix_equation:
            if item.type == Node.OPERATOR:
                stk.push(item)
            elif stk.top().type == Node.OPERAND:
                while not stk.empty() and stk.top().type == Node.OPERAND:
                    operand = stk.pop()
                    operator = stk.pop()
                    item = Node(Node.OPERAND, operate(operator.value, item.value, operand.value))
                stk.push(item)
            else:
                stk.push(item)
        return stk.top().value

    def input(self, char):
        self.__infix += char
        return self.__infix

    def get_infix(self):
        return self.__infix

    def clear_infix(self):
        self.__infix = ''

    def calculate(self):
        self.__prepare_infix()
        self.__infix_to_prefix()
        debug.log('prefix equation is: ' + str(self.__prefix_equation))
        result = self.__calculate_prefix()
        debug.log('result: ' + str(result))
        self.clear_infix()
        return result
