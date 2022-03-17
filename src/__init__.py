from flask import Blueprint
from flask_restful import Api

from src.todos.todo import Todo
from src.test.sample import sample
from src.users.user import User

blueprint = Blueprint("api", __name__)

api = Api(blueprint)

api.add_resource(Todo, '/todo')
api.add_resource(sample, '/sample')
api.add_resource(User, '/user')