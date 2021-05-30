"""
Access the application from command line
"""

from calculator.app import BodmasCalculatorApp, BodmasCalculatorError


def main():
    """
    Main method to start the app
    """
    calculator = BodmasCalculatorApp()
    print(calculator.help_message())
    quries_types = list(calculator.query_map.keys())
    quries_types.extend(['help', 'exit'])
    while True:
        query_type = input("\nChoose a query  from {}: ".format(quries_types)).strip()
        if query_type not in quries_types:
            print("\nInvalid query type. "
                  "Enter `help` to print help or enter `exit` to exit the application. "
                  "Please try again.")
            continue

        if query_type == 'exit':
            # Exit app
            break

        if query_type == 'help':
            # print help message
            print(calculator.help_message())
            continue

        if query_type == '1':
            try:
                expression, user_id = list(input("\nSelected query Type 1: Evaluate Expression.\n"
                                                 "Enter expression and user_id seperated "
                                                 "by ',' (comma): ").strip().split(','))
                expression = expression.strip()
                user_id = user_id.strip()
                value = calculator.run_query(query_type, expression=expression, user_id=user_id)
            except (BodmasCalculatorError, ValueError) as err:
                print("\nError: Invalid input: {}. Please try again".format(err))
                continue
            print("\n---  Value of the expression is {}  ---".format(value))

        if query_type == '2':
            try:
                user_id = input("\nSelected query Type 2: Get most used operator by a user.\n"
                                "Enter user_id: ").strip()
                user_id = user_id.strip()
                most_used_operator = calculator.run_query(query_type, user_id=user_id)
            except BodmasCalculatorError as err:
                print("\nError: Invalid UserID: {}. Please try again".format(err))
                continue
            print("\n---  Most used operator by user {} is `{}`  ---".format(user_id, most_used_operator))


if __name__ == '__main__':
    main()
