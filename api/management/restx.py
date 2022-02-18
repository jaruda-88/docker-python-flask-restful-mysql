from api import api
from flask_restx import Resource

@api.route("/")
class TestResource(Resource):
    def get(self):
        """ ddddd """
        pass
