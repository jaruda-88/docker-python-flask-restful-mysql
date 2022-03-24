from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database
from utils.function import get_add_hour_to_dt_now, encode_token, get_password_sha256_hash


db = database.DBHandler()


class Login(Resource):
    @swag_from('login.yml', validation=True)
    def post(self):
        resp = { 'resultCode': HTTPStatus.OK, 'resultMsg': '' }   

        try:
            rj = f_request.get_json()

            if rj is None:
                resp['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception("request data is empty")

            if rj['userid'] is None:
                resp['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("Not found userid")

            if rj['pw'] is None:
                resp['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("Not found pw")

            userid = rj['userid']
            pw = rj['pw']

            if userid == "":
                resp['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception("userid is empty")

            if pw == "":
                resp['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception("password is empty")

            # db 검색을 위해 비밀번호 암호화
            pw_hash = get_password_sha256_hash(pw)

            _flag, result = db.query('''SELECT * FROM tb_user WHERE userid=%s AND pw=%s;''', (userid, pw_hash))

            if _flag == False:
                resp['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception(f"{result[0]} : {result[1]}")

            if _flag and result is None or len(result) <= 0:
                resp['resultCode'] = HTTPStatus.FORBIDDEN
                raise Exception("userid or password does not match")

            payload = {
                'id': result[0]['id'],
                'userid': result[0]['userid'],
                'username': result[0]['username'],
                'exp': get_add_hour_to_dt_now(value=1,tz='Asia/Seoul')
            }

            token = encode_token(payload)

            resp['resultMsg'] = token
        except Exception as ex:
            resp['resultMsg'] = ex.args[0]

        if resp['resultCode'] == HTTPStatus.OK:
            return jsonify(resp)
        else:
            return resp, HTTPStatus.INTERNAL_SERVER_ERROR
