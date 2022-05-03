from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import databases as db
from utils.settings import DATABASE_CONFIG as con
from utils.function import (
    get_add_hour_to_dt_now, 
    encode_token, 
    get_password_sha256_hash,
    get_dt_now_to_str,
    is_blank_str
)


dbh = db.DBHandler(user=con['user'], host=con['host'], database=con['db_name'], pw=con['pw'], port=con['port'])


class Login(Resource):
    @swag_from('login.yml', validation=True)
    def post(self):
        response = { 'resultCode': HTTPStatus.INTERNAL_SERVER_ERROR }   

        try:
            rj = f_request.get_json()
            
            userid = rj.get('userid', None)
            pw = rj.get('pw', None)

            if is_blank_str(userid):
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('userid is empty')

            if is_blank_str(pw):
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('pw is empty')

            # db
            try:
                # 쿼리 작성
                sql = '''UPDATE tb_user 
                SET connected_at=%s 
                WHERE activate=%s AND userid=%s AND pw=%s;'''
                dt = get_dt_now_to_str()
                # db 검색을 위해 비밀번호 암호화
                pw_hash = get_password_sha256_hash(pw)
                value = (dt, 1, userid, pw_hash)
                # db 조회
                result = dbh.executer(sql=sql, value=value)

                if result == 0:
                    response['resultCode'] = HTTPStatus.FORBIDDEN
                    raise Exception("userid or password does not match")

                # 토큰 설정
                payload = {
                    'userid': userid,
                    'connected_at': dt,
                    'exp': get_add_hour_to_dt_now(value=1,tz='Asia/Seoul')
                }
                # 토큰 생성
                token = encode_token(payload)
            except Exception as ex:
                raise Exception(ex.args[0])
            else:
                response["resultCode"] = HTTPStatus.OK
                response['resultMsg'] = token
                return jsonify(response)

        except Exception as ex:
            response['resultMsg'] = ex.args[0]
            return response, HTTPStatus.INTERNAL_SERVER_ERROR
            
