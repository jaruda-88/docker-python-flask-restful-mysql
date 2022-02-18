from api.management import management_ns
from flask_restx import Resource

@management_ns.route("/")
class TestResource(Resource):
    def get(self):
        """ ddddd """
        pass
