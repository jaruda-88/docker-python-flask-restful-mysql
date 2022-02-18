from flask import Blueprint
from flask_restx import Api, Resource

blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(blueprint, version='1.0', title='rest api', description="my study")

management_ns = api.namespace("management", description="api")


@management_ns.route("/")
class TestResource(Resource):
    def get(self):
        """ ddddd """
        pass


