import operator
from collections import Counter


class InvalidExpressionError(Exception):
    def __init__(self, error):
        super().__init__("Invalid Exception: {}".format(error))


class BodmasSolver(object):
    """
    Solve any mathematical expression which is a sequence of BODMAS operations.
    Allowed caracters in the expression: '0123456789().*/+-^'
    Allowed operations:
        '+':    Addition
        '-':    Substraction
        '*':    Multiplication
        '/':    Division
        '^':    Power
    Sub expression can be put inside parantheses.
    """

    # Decimal places to consider if number if a float
    PRECISION = 8

    def __init__(self, expression_string):
        """
        Constructor
        ::parameter:    expression_string -> (str) mathematical expression
        """
        self.expression_string = expression_string.strip().replace(" ", "")
        self.possible_char = '0123456789().*/+-^'
        self.operator_counter = Counter()
        self.expression = self._validate_expression(self.expression_string)
        self.expression_copy = self.expression.copy()
        self.result = None

    def get_filtered_expression(self):
        """
        Returns the validated expression
        """
        return self.expression_copy

    def get_operator_counter(self):
        """
        Returns dict of operator
        """
        return self.operator_counter

    def _validate_expression(self, expression):
        """
        Validate the expression string.
        ::parameter : expression -> (str) BODMAS expression
        ::return    : exp_list   -> (list) validated and formated expression

        Perform following tasks:
        1. Raise error if string is empty.
        2. Raise error if string starts or ends with operator.
        3. Raise error if characters are not from range '0123456789().*/+-'
        4. Merge continous digits into single number.                           Ex.: '1+2.5'        -> ['1', '+', '2.5']
        5. Raise error if number have multile dots.                             Ex.: '10.10.10+3'   -> error
        6. Raise error if operator if followed by operator.                     Ex.: '10*/5'        -> error
        7. Raise error if number if followed by '('.                            Ex.: '10(5+4)'      -> error
        8. Raise error if there are imbalanced parentheses.                     Ex.: '(10+5*(5-(2)' -> error
        """
        if not expression:
            raise InvalidExpressionError("Empty expression.")
        if expression[0] in './+-*' or expression[-1] in '/.+-*':
            raise InvalidExpressionError("Must not start or ends with a operator.")
        for char in expression:
            if char not in self.possible_char:
                raise InvalidExpressionError("Unsupported character: `{}`. "
                                             "Supported caracters: `{}`"
                                             .format(char, self.possible_char))
        i = 0
        exp_list = []
        prev_char_was_num = False
        prev_char_was_op = False
        # in O(n)
        while i < len(expression):
            if expression[i].isnumeric():
                current = ""
                # Concatinate until next char is not a digit or not a dot
                while i < len(expression) and (expression[i].isnumeric() or expression[i] == '.'):
                    current += expression[i]
                    i += 1
                num_dots = [i for i in range(len(current)) if current[i] == '.']
                # if there are more than one dots, it is not a real number
                if len(num_dots) > 1:
                    raise InvalidExpressionError("Invalid number in expression: {}".format(current))
                # Only consider 'self.PRECISION' decimal places
                if len(num_dots) == 1:
                    current = current[:num_dots[0] + self.PRECISION + 1]
                # if ends with '.'' we add '0' to it
                if current[-1] == '.':
                    current += '0'
                prev_char_was_num = True
                prev_char_was_op = False
                exp_list.append(current)
            else:
                # If operator followed by operator -> raise error
                if prev_char_was_op and (expression[i] in '/*+-'):
                    raise InvalidExpressionError("Operator followed by operator.")
                # if digit is followed by '(' raise error
                if prev_char_was_num and expression[i] == '(':
                    raise InvalidExpressionError("Digit must not followed by `(`.")
                exp_list.append(expression[i])
                prev_char_was_num = False
                prev_char_was_op = True if expression[i] in '/*+-' else False
                i += 1

        parentheses_stk = []
        # Check if parentheses are balanced or not
        for char in exp_list:
            if char == '(':
                parentheses_stk.append(char)
            elif char == ')':
                if not parentheses_stk:
                    raise InvalidExpressionError("Imbalanced parentheses")
                close = parentheses_stk.pop(-1)
                if close != '(':
                    raise InvalidExpressionError("Imbalanced parentheses")
        if parentheses_stk:
            raise InvalidExpressionError("Imbalanced parentheses")

        # Final expression must have odd number of elements.
        if len(exp_list) % 2 == 0:
            raise InvalidExpressionError("Uneven expression")
        return exp_list

    def _evaluate_operation(self, num1, operation, num2):
        """
        Perform Add, Sub, Mul, Pow and Div operation.
        ::parameter : num1  -> (str) LHS number
        ::parameter : operation  -> (str) Operation to perform
        ::parameter : num2  -> (str) RHS number
        ::return   : num3 -> Output after operation
        """
        ops = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '^': operator.pow,
            '/': operator.truediv
        }
        self.operator_counter[operation] += 1
        try:
            num3 = ops[operation](float(num1), float(num2))
        except ZeroDivisionError:
            raise InvalidExpressionError("Divide by zero involved.")
        return str(num3)

    def _find_and_evaluate_operation(self, operation):
        """
        Interate through the expression and execute spectific operation.
        ::parameter : operation -> (str) Operation to perform
        ::return    : True if found and executed the operation else False
        """
        count = 1
        repeat = False
        while count < len(self.expression) - 1:
            if self.expression[count] in operation and not (self.expression[count + 1] in '()' or self.expression[count - 1] in '()'):
                self.expression[count - 1] = self._evaluate_operation(self.expression[count - 1],
                                                                      self.expression[count],
                                                                      self.expression[count + 1])
                self.expression = self.expression[:count] + self.expression[count + 2:]
                repeat = True
            count += 1
        return repeat

    def _remove_parentheses_around_number(self):
        """
        Interate through the expression and remove parentheses around single number.
        Example: "3+(4)" -> "3+4"
        ::return    : True if found and removed parentheses else False
        """
        count = 0
        repeat = False
        while count < len(self.expression) - 1:
            if self.expression[count] == '(' and self.expression[count + 2] == ')':
                self.expression = self.expression[:count] + \
                    [self.expression[count + 1]] + \
                    self.expression[count + 3:]
                repeat = True
            count += 1
        return repeat

    def evaluate(self):
        """
        Calculate the value of expression using BODMAS.
        ::return    : self.result -> Final value of expression
        """
        try:
            # Loop until one element is left i.e. the final value of expression
            while len(self.expression) != 1:
                repeat = False
                # Remove continuos open and close parentheses
                repeat = self._remove_parentheses_around_number()
                if repeat:
                    continue
                # Evaluate Power
                repeat = self._find_and_evaluate_operation("^")
                if repeat:
                    continue
                # Evaluate Multiplcation and Division
                repeat = self._find_and_evaluate_operation("*/")
                if repeat:
                    continue
                # Evaluate Addition add Substraction
                _ = self._find_and_evaluate_operation("+-")

            self.result = float(self.expression[0])
            return self.result
        except InvalidExpressionError as err:
            raise err
