from api import management_ns
from flask_restx import Resource


@management_ns.route("/test")
class TestResource(Resource):
    def get(self):
        """ ddddd """
        pass