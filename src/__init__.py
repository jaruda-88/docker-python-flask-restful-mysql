from flask import Blueprint
from flask_restful import Api
from utils.settings import BUILD

blueprint = Blueprint("api", __name__)
api = Api(blueprint)


from src.users.user import User
from src.signin.login import Login
from src.boards.board import Board

# if BUILD['type'] != 'server':
#     from src.todos.todo import Todo
#     from src.test.sample import sample
#     api.add_resource(Todo, '/todo')
#     api.add_resource(sample, '/sample')
api.add_resource(User, '/user')
api.add_resource(Login, '/user/login')
api.add_resource(Board, '/board')