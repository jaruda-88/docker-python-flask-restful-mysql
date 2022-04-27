from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.databases as db
from utils.settings import DATABASE_CONFIG as con
from src.users.user_methods import (
    userinfo, 
    registration,
    edit,
)
from utils.function import (
    is_token,
    get_password_sha256_hash, 
    get_dt_now_to_str,
    is_blank_str
)


dbh = db.DBHandler(host=con['host'], user=con['user'], pw=con['pw'], database=con['db_name'], port=con['port'])


class User(Resource):
    @swag_from(registration)
    def post(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

        try:
            rj = f_request.get_json()

            userid = rj.get('userid', None)
            pw = rj.get('pw', None)
            usernm = rj.get('username', None)

            if is_blank_str(userid):
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('userid is empty')

            if is_blank_str(pw):
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('pw is empty')

            if usernm is None:
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('usernm is empty')

            # db
            try:    
                # 쿼리 작성, 유니크 설정하지않고 userid 중복 체크
                sql = '''INSERT INTO tb_user (userid, username, pw, create_at, update_at) 
                SELECT %s,%s,%s,%s,%s
                FROM 
                DUAL WHERE NOT EXISTS(SELECT userid FROM tb_user WHERE userid=%s);'''
                dt = get_dt_now_to_str()
                # 비밀번호 암호화
                pw_hash = get_password_sha256_hash(pw)
                value = (userid, usernm, pw_hash, dt, dt, userid)
                # db 조회
                result = dbh.executer(sql=sql, value=value, last_id=True)

                # insert 실패
                if result == 0:
                    response["resultCode"] = HTTPStatus.FORBIDDEN
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
            
            # db
            try:
                # 쿼리 작성
                sql = '''SELECT id, userid, username, connected_at
                FROM tb_user
                WHERE activate=%s AND userid=%s'''
                # db 조회
                result = dbh.query(sql=sql, value=(1, payload['userid']), all=False)

                if not result:
                    response['resultCode'] = HTTPStatus.INTERNAL_SERVER_ERROR
                    raise Exception('This is a deactivated account')
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
                is_token(f_request.headers)
            except Exception as ex:
                response['resultCode'] = HTTPStatus.UNAUTHORIZED
                raise Exception(ex.args[0])

            rj = f_request.get_json()

            id = rj.get('id', None)
            userid = rj.get('userid', None)
            username = rj.get('username', None)
            pw = rj.get('pw', None)

            if id is None:
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('id is empty')

            if is_blank_str(userid):
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('userid is empty')

            if is_blank_str(pw):
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('pw is empty')

            if username is None:
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('username is empty')

            # db
            try:
                # 쿼리 작성, userid 중복 체크
                select_sql = "SELECT userid FROM tb_user WHERE userid='{}';".format(userid)
                # db 조회
                select_result = dbh.query(sql=select_sql, all=False)

                if select_result:
                    response["resultCode"] = HTTPStatus.FORBIDDEN
                    raise Exception('already exist userid')

                # 쿼리 작성, id(pk)에 해당하는 데이터 UPDATE
                update_sql ='''UPDATE tb_user
                SET userid=%s, username=%s, pw=%s, update_at=%s
                WHERE id=%s;'''
                # 비밀번호 암호화
                pw_hash = get_password_sha256_hash(pw)
                update_value = (userid, username, pw_hash, get_dt_now_to_str(), int(id))
                # db 조회
                update_result = dbh.executer(sql=update_sql, value=update_value)

                # UPDATE 실패
                if update_result == 0:
                    response['resultCode'] = HTTPStatus.FORBIDDEN
                    raise Exception('id(pk) does not match')
            except Exception as ex:
                raise Exception(ex.args[0])
            else:
                response["resultCode"] = HTTPStatus.OK
                response['resultMsg'] = "Ok"
                return jsonify(response)

        except Exception as ex:
            response['resultMsg'] = ex.args[0]
            return response, HTTPStatus.INTERNAL_SERVER_ERROR