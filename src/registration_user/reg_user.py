from http import HTTPStatus
from unittest import result
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database
import hashlib


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

            # INSERT INTO project1.tb_user (userid, username, pw, create_at) SELECT 'test','test','test',SYSDATE() FROM DUAL WHERE NOT EXISTS (SELECT * FROM tb_user WHERE userid='test');
            _flag, tb_user = db.query( '''INSERT INTO tb_user (user)''' )

            # if _flag == False:
            #     raise Exception(f"{result[0]} : {result[1]}")            

            # list_of_userid = [ str(user['userid']) for user in tb_user ] 

            # if userid in list_of_userid:
            #     raise Exception('userid already registered')

            pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

            return ""

        except Exception as ex:
            return jsonify(ex.args[0])