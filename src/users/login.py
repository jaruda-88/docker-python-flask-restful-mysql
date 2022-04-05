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
        response = { 'resultCode': HTTPStatus.OK, 'resultMsg': '' }   

        try:
            rj = f_request.get_json()

            if rj is None:
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception("request data is empty")

            if rj['userid'] is None:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("Not found userid")

            if rj['pw'] is None:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("Not found pw")

            userid = rj['userid']
            pw = rj['pw']

            if userid == "":
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception("userid is empty")

            if pw == "":
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception("password is empty")

            # db 검색을 위해 비밀번호 암호화
            pw_hash = get_password_sha256_hash(pw)

            # 쿼리 작성
            sql = '''SELECT * FROM tb_user WHERE userid=%s AND pw=%s;'''
            _flag, result = db.query(sql, (userid, pw_hash))

            if _flag == False:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception(f"{result[0]} : {result[1]}")

            if _flag and result is None or len(result) <= 0:
                response['resultCode'] = HTTPStatus.FORBIDDEN
                raise Exception("userid or password does not match")

            # 토큰 설정
            payload = {
                'id': result[0]['id'],
                'userid': result[0]['userid'],
                'username': result[0]['username'],
                'exp': get_add_hour_to_dt_now(value=1,tz='Asia/Seoul')
            }

            # 토큰 생성
            token = encode_token(payload)

            response['resultMsg'] = token
        except Exception as ex:
            response['resultMsg'] = ex.args[0]

        if response['resultCode'] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR
