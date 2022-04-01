from flask import Blueprint
from flask_restful import Api


blueprint = Blueprint("api", __name__)
api = Api(blueprint)


from src.todos.todo import Todo
from src.test.sample import sample
from src.users.user import User
from src.users.registration import Registration
from src.users.login import Login
from src.boards.board import Board


api.add_resource(Todo, '/todo')
api.add_resource(sample, '/sample')
api.add_resource(User, '/user')
api.add_resource(Registration, '/user/registration')
api.add_resource(Login, '/user/login')
api.add_resource(Board, '/board')