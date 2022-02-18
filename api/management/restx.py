from importlib.resources import Resource
from api.management.model import management_ns
from flask_restx import Resource


@management_ns.route("/test")
class TestResource(Resource):
    def get(self):
        """ test """
        pass