from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
from utils.function import get_dt_now_to_str, get_password_sha256_hash
import utils.database as database


db = database.DBHandler()


class Registration(Resource):
    @swag_from('registration.yml', validation=True)
    def post(self):
        """ 회원가입 """
        response = { "resultCode" : HTTPStatus.OK, "resultMsg" : 'Ok' }
        try:
            rj = f_request.get_json()

            if rj is None:
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception("request data is empty")

            if rj['userid'] is None:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("Not found userid")

            if rj['username'] is None:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("Not found username")

            if rj['pw'] is None:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("Not found pw")

            userid = rj['userid']
            usernm = rj['username']
            pw = rj['pw']

            if userid == "":
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('userid is empty')
            
            if pw == "":
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('password is empty')

            # 비밀번호 암호화
            pw_hash = get_password_sha256_hash(pw)

            # 쿼리 작성, 유니크 설정하지않고 userid 중복 체크
            _flag, result = db.executer('''INSERT INTO tb_user (userid, username, pw, create_at) 
            SELECT %s,%s,%s,%s 
            FROM 
            DUAL WHERE NOT EXISTS(SELECT * FROM tb_user WHERE userid=%s);''', 
            (userid, usernm, pw_hash, get_dt_now_to_str(), userid))

            # db 쿼리 실패
            if _flag == False:
                response["resultCode"] = HTTPStatus.NOT_FOUND
                raise Exception(f"{result[0]} : {result[1]}")
            
            # insert 성공 시 1
            # insert 실패 시 0
            if type(result) is int and bool(result) == False: 
                response["resultCode"] = HTTPStatus.FORBIDDEN
                raise Exception('userid already registered')
            
        except Exception as ex:
            response["resultMsg"] = ex.args[0]

        if response["resultCode"] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR