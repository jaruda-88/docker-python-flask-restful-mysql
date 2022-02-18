from flask_restx import Resource, Namespace

api = Namespace("management", description="api")

@api.route("/")
class TestResource(Resource):
    def get(self):
        """ ddddd """
        pass
