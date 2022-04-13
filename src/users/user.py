from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database
from src.users.user_methods import (
    userinfo, 
    registration,
    edit,
)
from utils.function import (
    check_token, 
    get_password_sha256_hash, 
    get_dt_now_to_str,
    check_body_request
)


db = database.DBHandler()


class User(Resource):
    @swag_from(registration)
    def post(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg" : 'Ok' }

        try:
            rj = f_request.get_json()

            # request data 확인
            response['resultCode'], response['resultMsg'] = check_body_request( rj, ('userid', 'pw') )
            if response['resultCode'] != HTTPStatus.OK:
                raise Exception(response['resultMsg'])

            userid = rj['userid']
            usernm = rj['username'] if rj['username'] else ''
            pw = rj['pw']

            # 비밀번호 암호화
            pw_hash = get_password_sha256_hash(pw)

            dt = get_dt_now_to_str()

            # 쿼리 작성, 유니크 설정하지않고 userid 중복 체크
            _flag, result = db.executer('''INSERT INTO tb_user (userid, username, pw, create_at, update_at) 
            SELECT %s,%s,%s,%s,%s
            FROM 
            DUAL WHERE NOT EXISTS(SELECT userid FROM tb_user WHERE userid=%s);''', 
            (userid, usernm, pw_hash, dt, dt, userid))

            # db 조회 실패
            if _flag == False:
                response["resultCode"] = HTTPStatus.NOT_FOUND
                raise Exception(f"{result[0]} : {result[1]}")
            
            # insert 성공 시 1
            # insert 실패 시 0
            if type(result) is int and bool(result) == False: 
                response["resultCode"] = HTTPStatus.FORBIDDEN
                raise Exception('userid already registered')

            response["resultCode"] = HTTPStatus.OK
            response["resultMsg"] = 'Ok'
            
        except Exception as ex:
            response["resultMsg"] = ex.args[0]

        if response["resultCode"] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR

            
    @swag_from(userinfo)
    def get(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg" : '' }

        try:
            # 토큰 화인
            response['resultCode'], payload = check_token(f_request.headers)
            if response['resultCode'] != HTTPStatus.OK:
                raise Exception(payload)

            # 쿼리 작성
            sql = '''SELECT id, userid, username, connected_at 
            FROM tb_user 
            WHERE activate=1 AND userid=%s;'''
            _flag, result = db.query(sql, payload['userid'])

            # db 조회 실패
            if _flag == False:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception(f"{result[0]} : {result[1]}")
            
            # SELECT 실패
            if _flag and result is None or len(result) <= 0:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("not user data")

            response["resultCode"] = HTTPStatus.OK
            response["resultMsg"] = result[0]
                
        except Exception as ex:
            response["resultMsg"] = ex.args[0]

        if response["resultCode"] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR


    @swag_from(edit)
    def put(self):
        response = { "resultCode": HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg": '' }
        
        try:
            # 토큰 확인
            response['resultCode'], payload = check_token(f_request.headers)
            if response['resultCode'] != HTTPStatus.OK:
                raise Exception(payload)

            rj = f_request.get_json()

            # request data 확인
            response['resultCode'], response['resultMsg'] = check_body_request( rj, ('id', 'userid', 'pw') )
            if response['resultCode'] != HTTPStatus.OK:
                raise Exception(response['resultMsg'])

            id = rj['id']
            userid = rj['userid']
            username = rj['username'] if rj['username'] else ''
            pw = rj['pw']

            # 비밀번호 암호화
            pw_hash = get_password_sha256_hash(pw)

            dt = get_dt_now_to_str()

            # 쿼리 작성
            sql ='''UPDATE tb_user 
            SET userid=%s, username=%s, pw=%s, update_at=%s 
            WHERE id=%s AND NOT pw=%s;'''
            _flag, result = db.executer(sql, (userid, username, pw_hash, dt, int(id), pw_hash))

            # db 조회 실패
            if _flag == False:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception(f'{result[0]} : {result[1]}')

            # UPDATE 실패
            if _flag and bool(result) == False:
                response['resultCode'] = HTTPStatus.FORBIDDEN
                raise Exception('Password is the same as before')
            
            response["resultCode"] = HTTPStatus.OK
            response['resultMsg'] = "Ok"

        except Exception as ex:
            response['resultMsg'] = ex.args[0]

        if response['resultCode'] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR


    