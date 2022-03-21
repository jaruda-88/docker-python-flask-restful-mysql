from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
from utils.function import get_dt_now_to_str
import utils.database as database
import hashlib


db = database.DBHandler()


class Registration(Resource):
    @swag_from('registration.yml', validation=True)
    def post(self):
        resp = { "resultCode" : HTTPStatus.OK, "resultMsg" : '' }
        try:
            rj = f_request.get_json()
            # auth = f_request.headers['Authorization']
            # auth = f_request.headers.get('Authorization')

            if rj is None:
                resp['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception("request data is empty")

            userid = rj['userid']
            usernm = rj['username']
            pw = rj['pw']

            if userid == "":
                resp["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('userid is empty')
            
            if pw == "":
                resp["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception('password is empty')

            # 비밀번호 암호화
            pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

            # 쿼리, 유니크 설정하지않고 userid 중복 체크
            _flag, result = db.executer('''INSERT INTO tb_user (userid, username, pw, create_at) 
            SELECT %s,%s,%s,%s 
            FROM 
            DUAL WHERE NOT EXISTS(SELECT * FROM tb_user WHERE userid=%s);''', 
            (userid, usernm, pw_hash, get_dt_now_to_str(), userid))

            # db 쿼리 실패
            if _flag == False:
                resp["resultCode"] = HTTPStatus.NOT_FOUND
                raise Exception(f"{result[0]} : {result[1]}")
            
            # insert 성공 시 1
            # insert 실패 시 0
            if type(result) is int and bool(result) == False: 
                resp["resultCode"] = HTTPStatus.FORBIDDEN
                raise Exception('userid already registered')
            
            # 회원등록 성공
            resp["resultMsg"] = 'success'
                
        except Exception as ex:
            resp["resultMsg"] = ex.args[0]

        if resp["resultCode"] == HTTPStatus.OK:
            return jsonify(resp)
        else:
            return resp, HTTPStatus.INTERNAL_SERVER_ERROR