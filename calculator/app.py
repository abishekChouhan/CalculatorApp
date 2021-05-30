from .bodmas_solver import BodmasSolver, InvalidExpressionError


class BodmasCalculatorError(Exception):
    def __init__(self, error):
        super().__init__(error)


class UserData(object):
    """
    Stores data of one user.
    """

    def __init__(self, user_id):
        """
        Constructor
        ::parameter:    user_id -> (int) UserID of a User
        """
        self.user_id = user_id
        self.expressions = []
        self.most_used_operator = 0
        self.operator_counter = {key: 0 for key in '+-*/^'}

    def get_most_used_operator(self):
        """
        Returns most used operator.
        """
        return self.most_used_operator

    def execute_expression(self, expression):
        """
        Execute the expression and keep note of most used operator.
        ::parameter : expression  -> (str) mathematical expressions.
        ::return    : output -> Final value of expression
        """
        try:
            solver = BodmasSolver(expression)
            self.expressions.append(solver.get_filtered_expression())
            output = solver.evaluate()
            operator_counter = solver.get_operator_counter()
            max_value = -1
            for key in self.operator_counter.keys():
                self.operator_counter[key] += operator_counter[key]
                if self.operator_counter[key] > max_value:
                    max_value = self.operator_counter[key]
                    self.most_used_operator = key
            return output
        except InvalidExpressionError as err:
            raise ValueError(err)


class BodmasCalculatorApp(object):
    """
    The application allow users to solve mathematical expressions.
    The mathematical expression can be any sequence of BODMAS operations.
    """

    def __init__(self):
        self.users = {}
        self.query_map = {
            '1': self._query_1,
            '2': self._query_2
        }

    def _query_1(self, expression, user_id):
        """
        Query type 1. Evaluates a mathematical expression.
        ::paramaeter    : expression -> (str) Mathematical expression
        ::paramaeter    : user_id     -> (int | numric str) UserID
        ::return        : the value of the expression.
        """
        if not isinstance(user_id, int):
            if isinstance(user_id, str) and user_id.isnumeric():
                user_id = int(user_id)
            else:
                raise BodmasCalculatorError("`user_id` must be a natural number")
        if not isinstance(expression, str):
            raise BodmasCalculatorError("`expression` must be a string")
        if user_id not in self.users.keys():
            self.users[user_id] = UserData(user_id)
        try:
            value = self.users[user_id].execute_expression(expression)
        except ValueError as err:
            raise BodmasCalculatorError(err)
        return value

    def _query_2(self, user_id):
        """
        Query type 2. Most used mathematical operator by the User.
        ::parameter    : usr_id -> (int | numric str) UserID
        ::return        : Most used operator
        """
        if not isinstance(user_id, int):
            if isinstance(user_id, str) and user_id.isnumeric():
                user_id = int(user_id)
            else:
                raise BodmasCalculatorError("`user_id` must be a natural number")
        if not self.users.get(user_id):
            raise BodmasCalculatorError("User with user_id `{}` does not exist".format(user_id))
        return self.users[user_id].get_most_used_operator()

    def run_query(self, query_type, **kwargs):
        """
        Execute a query
        ::parameter     : query_type -> (str) Type of query to execute
        ::parameter     : **kwargs   -> Any number of keyword arguments
        ::return        : return the value of the query
        """
        try:
            return self.query_map[query_type](**kwargs)
        except (TypeError, BodmasCalculatorError) as err:
            raise BodmasCalculatorError(err)

    def help_message(self):
        """
        Construct help message
        """
        _help = "{0}\n".format(self.__doc__)
        _help += "User can perform {} types of queries\n".format(len(self.query_map.keys()))
        for query_type in self.query_map.keys():
            _help += self.query_map[query_type].__doc__
            _help += '\n'
        return _help
