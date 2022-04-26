from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database
import utils.database2
from src.users.user_methods import (
    userinfo, 
    registration,
    edit,
)
from utils.function import (
    is_token,
    check_token, 
    get_password_sha256_hash, 
    get_dt_now_to_str,
    check_body_request,
    is_blank_str
)
from utils.settings import DATABASE_CONFIG as con


#db = database.DBHandler()
db2 = utils.database2.DBHandler(host=con['HOST'], user=con['USER'], pw=con['PASSWORD'], database=con['DB'])


class User(Resource):
    @swag_from(registration)
    def post(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

        try:
            rj = f_request.get_json()

            userid = rj['userid']
            pw = rj['pw']
            usernm = rj['username']

            if is_blank_str(userid):
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('userid is empty')

            if is_blank_str(pw):
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('pw is empty')

            # 비밀번호 암호화
            pw_hash = get_password_sha256_hash(pw)

            dt = get_dt_now_to_str()

            # 쿼리 작성
            try:    
                # 유니크 설정하지않고 userid 중복 체크
                sql = '''INSERT INTO tb_user (userid, username, pw, create_at, update_at) 
                SELECT %s,%s,%s,%s,%s
                FROM 
                DUAL WHERE NOT EXISTS(SELECT userid FROM tb_user WHERE userid=%s);'''
                value = (userid, usernm, pw_hash, dt, dt, userid)
                # db 조회
                result = db2.executer(sql=sql, value=value, last_id=True)

                # insert 실패
                if result == 0:
                    raise Exception('already exist account')
            except Exception as ex:
                raise Exception(ex.args[0])
            else:
                response["resultCode"] = HTTPStatus.OK
                response["resultMsg"] = result
                return jsonify(response)
            
        except Exception as ex:
            response["resultMsg"] = ex.args[0]
            return response, HTTPStatus.INTERNAL_SERVER_ERROR
            

            
    @swag_from(userinfo)
    def get(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

        try:
            # 토큰 화인
            try:
                payload = is_token(f_request.headers)
            except Exception as ex:
                response['resultCode'] = HTTPStatus.UNAUTHORIZED
                raise Exception(ex.args[0])
            
            # 쿼리 작성
            try:
                sql = '''SELECT id, userid, username, connected_at
                FROM tb_user
                WHERE activate=%s AND userid=%s'''
                # db 조회
                result = db2.query(sql=sql, value=(1, payload['userid']), all=False)
            except Exception as ex:
                raise Exception(ex.args[0])
            else:
                response["resultCode"] = HTTPStatus.OK
                response["resultMsg"] = result
                return jsonify(response)
                
        except Exception as ex:
            response["resultMsg"] = ex.args[0]
            return response, HTTPStatus.INTERNAL_SERVER_ERROR


    @swag_from(edit)
    def put(self):
        response = { "resultCode": HTTPStatus.INTERNAL_SERVER_ERROR }
        
        try:
            # 토큰 화인
            try:
                payload = is_token(f_request.headers)
            except Exception as ex:
                response['resultCode'] = HTTPStatus.UNAUTHORIZED
                raise Exception(ex.args[0])

            rj = f_request.get_json()

            id = rj['id']
            userid = rj['userid']
            username = rj['username']
            pw = rj['pw']

            if is_blank_str(userid):
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('userid is empty')

            if is_blank_str(pw):
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('pw is empty')

            # 비밀번호 암호화
            pw_hash = get_password_sha256_hash(pw)

            dt = get_dt_now_to_str()

            # 쿼리 작성
            try:
                if payload['userid'] == userid:
                    sql ='''UPDATE tb_user 
                    SET username=%s, pw=%s, update_at=%s 
                    WHERE id=%s;'''
                    value = (username, pw_hash, dt, int(id))
                else:
                    sql ='''UPDATE tb_user 
                    SET userid=%s, username=%s, pw=%s, update_at=%s 
                    WHERE NOT userid=%s AND id=%s;'''
                    value = (userid, username, pw_hash, dt, userid, int(id))
                # db 조회
                result = db2.executer(sql=sql, value=value)

                # UPDATE 실패
                if result == 0:
                    response['resultCode'] = HTTPStatus.FORBIDDEN
                    raise Exception('already userid')
            except Exception as ex:
                raise Exception(ex.args[0])
            else:
                response["resultCode"] = HTTPStatus.OK
                response['resultMsg'] = "Ok"
                return jsonify(response)

        except Exception as ex:
            response['resultMsg'] = ex.args[0]
            return response, HTTPStatus.INTERNAL_SERVER_ERROR