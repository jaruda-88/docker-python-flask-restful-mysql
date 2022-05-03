from http import HTTPStatus
from flask import jsonify, request as f_request
from flask_restful import Resource
from flasgger import Swagger, swag_from
import databases as db
from utils.settings import DATABASE_CONFIG as con
from src.boards.board_methods import (
    writing,
    written_list,
    edit
    )
from utils.function import (
    get_dt_now_to_str,
    is_blank_str, 
    is_token
    )


dbh = db.DBHandler(host=con['host'], user=con['user'], port=con['port'], database=con['db_name'], pw=con['pw'])


class Board(Resource):
    @swag_from(writing)
    def post(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

        try:
            # 토큰 확인
            try:
                is_token(f_request.headers)
            except Exception as ex:
                response['resultCode'] = HTTPStatus.UNAUTHORIZED
                raise Exception(ex.args[0])

            rj = f_request.get_json()

            writer = rj.get('writer', None)
            title = rj.get('title', None)
            content= rj.get('content', '')

            if is_blank_str(writer):
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('writer is empty')      

            if is_blank_str(title):
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('title is empty')        

            # 로그인 유저와 작성자 매칭 확인
            # if payload['userid'] and writer != payload['userid']:
            #     response["resultCode"] = HTTPStatus.INTERNAL_SERVER_ERROR
            #     raise Exception("does not match writer(userid)")

            # db
            try:
                # 쿼리 작성
                sql = '''INSERT INTO tb_board (writer, title, content, create_at, update_at)
                VALUES(%s, %s, %s, %s, %s);'''
                dt = get_dt_now_to_str()
                value = (writer, title, content, dt, dt)
                # db 조회
                result = dbh.executer(sql=sql, value=value, is_lastrowid=True)

                if result == 0:
                    response['resultCode'] = HTTPStatus.FORBIDDEN
                    raise Exception('post fail')
            except Exception as ex:
                raise Exception(ex.args[0])
            else:
                response['resultCode'] = HTTPStatus.OK
                response['resultMsg'] = result
                return jsonify(response)        

        except Exception as ex:
            response['resultMsg'] = ex.args[0]
            return response, HTTPStatus.INTERNAL_SERVER_ERROR 
 
    
    @swag_from(written_list)
    def get(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

        try:
            # 토큰 확인
            try:
                payload = is_token(f_request.headers)
            except Exception as ex:
                response['resultCode'] = HTTPStatus.UNAUTHORIZED
                raise Exception(ex.args[0])

            # db
            try:
                # 쿼리 작성
                sql = f'''SELECT id, writer, title, update_at
                FROM tb_board
                WHERE writer='{payload['userid']}';'''
                # db 조회
                result = dbh.query(sql=sql)
            except Exception as ex:
                raise Exception(ex.args[0])
            else:
                response['resultCode'] = HTTPStatus.OK
                response['resultMsg'] = result
                return jsonify(response)

        except Exception as ex:
            response['resultMsg'] = ex.args[0]
            return response, HTTPStatus.INTERNAL_SERVER_ERROR


    @swag_from(edit)
    def put(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

        try:
            # 토큰 확인
            try:
                is_token(f_request.headers)
            except Exception as ex:
                response['resultCode'] = HTTPStatus.UNAUTHORIZED
                raise Exception(ex.args[0])

            rj = f_request.get_json()

            id = rj.get('id', None)
            title = rj.get('title', None)
            writer = rj.get('writer', None)
            content = rj.get('content', '')

            if is_blank_str(id):
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('id is empty')

            if is_blank_str(title):
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('title is empty')

            if is_blank_str(writer):
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('writer is empty')

            # db
            try:
                # 쿼리 작성
                sql = '''UPDATE tb_board
                SET writer=%s, title=%s, content=%s, update_at=%s
                WHERE id=%s;'''
                dt = get_dt_now_to_str()
                value = (writer, title, content, dt, int(id))
                # db 조회
                result = dbh.executer(sql=sql, value=value)

                if result == 0:
                    response['resultCode'] = HTTPStatus.FORBIDDEN
                    raise Exception('edit fail')
            except Exception as ex:
                raise Exception(ex.args[0])
            else:
                response['resultCode'] = HTTPStatus.OK
                response['resultMsg'] = 'Ok'
                return jsonify(response)
        
        except Exception as ex:
            response['resultMsg'] = ex.args[0]
            return response, HTTPStatus.INTERNAL_SERVER_ERROR
            