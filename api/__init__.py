from flask import Blueprint
from flask_restx import Api, Namespace

blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(blueprint, version='1.0', title='rest api', description="my study")

management_ns = Namespace("management", description="api")

api.add_namespace(management_ns, path="/management")

