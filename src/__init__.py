from flask import Blueprint
from flask_restful import Api

from src.todos.todo import Todo

blueprint = Blueprint("api", __name__)

api = Api(blueprint)

api.add_resource(Todo, '/todo')