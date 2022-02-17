from ensurepip import version
from turtle import title
from flask import Blueprint
from flask_restplus import Api

blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(blueprint, version='1.0', title='rest api', description="my study")

management_ns  = api.namespace('management', description='ㅎㅎ')
