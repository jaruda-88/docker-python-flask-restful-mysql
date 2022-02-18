from api.management import api as ns
from flask_restx import Resource, Namespace

#api = Namespace("management", description="api")

@ns.route("/")
class TestResource(Resource):
    def get(self):
        """ ddddd """
        pass
