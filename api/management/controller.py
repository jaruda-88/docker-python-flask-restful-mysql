from flask_restx import Resource, Namespace
from .dto import test

api = Namespace("management", description="api")


@api.route("/")
class TestResource(Resource):
    @api.marshal_with(test)
    def get(self):
        """ get test """
        return "test"
