from http import HTTPStatus
from unittest import result
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database


db = database.DBHandler()


class RegistrationUser(Resource):
    @swag_from('reg_user.yml', validation=True)
    def post(self):
        try:
            rj = f_request.get_json()

            userid = rj['userid']
            usernm = rj['username']
            pw = rj['pw']

            if userid == "":
                raise Exception('userid is empty')
            
            if pw == "":
                raise Exception('password is empty')

            _flag, tb_user = db.query( '''SELECT * FROM tb_user;''' )

            if _flag == False:
                raise Exception(f"{result[0]} : {result[1]}")            

            return ""

        except Exception as ex:
            return jsonify(ex.args[0])