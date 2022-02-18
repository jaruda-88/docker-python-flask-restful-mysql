from .restx import api as ns
from flask_restx import Resource


@ns.route("/tttttttt")
class TestResource(Resource):
    def get(self):
        """ ddddd """
        pass