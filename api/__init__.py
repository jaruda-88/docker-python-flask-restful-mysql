from flask import Blueprint
from flask_restful import Api

from api.todos.todo import Todo

blueprint = Blueprint("api", __name__, url_prefix="/api")

api = Api(blueprint)

api.add_resource(Todo, '/Todo')