import imp
from flask import Blueprint
from flask_restx import Api
from api.management import management_ns

blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(blueprint, version='1.0', title='rest api', description="my study")

api.add_namespace(management_ns, "/management")



