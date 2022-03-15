from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database


db = database.DBHandler()


class RegistrationUser(Resource):
    @swag_from('reg_user.yml', validation=True)
    def post(self):
        pass