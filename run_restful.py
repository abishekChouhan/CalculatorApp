"""
Access the application from REST API.
"""

from flask import Flask
from flask_restful import reqparse, Api, Resource
from calculator.app import BodmasCalculatorApp, BodmasCalculatorError

# Init Flask app
app = Flask(__name__)
api = Api(app)

calculator = BodmasCalculatorApp()

# Parse argument for POST request
parser = reqparse.RequestParser()
parser.add_argument('expression')
parser.add_argument('user_id')


class ExecuteExpression(Resource):
    """
    Accepts POST request for evaluating a metametical expression
    """

    def post(self):
        args = parser.parse_args()
        try:
            output = calculator.run_query(query_type='1',
                                          expression=args['expression'],
                                          user_id=args['user_id'])
        except BodmasCalculatorError as err:
            return str(err), 400
        return {"value": output}


class MostUsedOperator(Resource):
    """
    Accepts GET request for returning most used operator by an user.
    """

    def get(self, user_id):
        try:
            output = calculator.run_query(query_type='2', user_id=user_id)
        except BodmasCalculatorError as err:
            return str(err), 400
        return {"most-used-operator": output}


class HelpMessage(Resource):
    """
    Return help message
    """

    def get(self):
        # TO-DO: format help message properly
        try:
            output = calculator.help_message()
        except BodmasCalculatorError as err:
            return str(err), 400
        return {"help": output}


# Adding routes
api.add_resource(ExecuteExpression, '/execute')
api.add_resource(MostUsedOperator, '/most-used-operator/<user_id>')
api.add_resource(HelpMessage, '/help')

if __name__ == '__main__':
    app.run(debug=False)
