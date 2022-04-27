from flask import Blueprint
from flask_restful import Api

blueprint = Blueprint("api", __name__)
api = Api(blueprint)


from src.users.user import User
from src.signin.login import Login
from src.boards.board import Board
from src.comments.comment import Comment

api.add_resource(User, '/user')
api.add_resource(Login, '/user/login')
api.add_resource(Board, '/board')
api.add_resource(Comment, '/board/comment')
