from http import HTTPStatus
from math import fabs
from unittest import result
from urllib import response
from flask import jsonify, request as f_request
from flask_restful import Resource
from flasgger import Swagger, swag_from
import utils.database as database
import pymysql
from src.boards.board_methods import (
    writing,
    delete_post,
    written_list,
    edit
    )
from utils.function import (
    get_dt_now_to_str, 
    check_token,
    check_body_request
    )


db = database.DBHandler()


class Board(Resource):
    @swag_from(writing)
    def post(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg" : '' }

        try:
            # 토큰 확인
            response['resultCode'], payload = check_token(f_request.headers)
            if response['resultCode'] != HTTPStatus.OK:
                raise Exception(payload)

            rj = f_request.get_json()

            # request data 확인
            response['resultCode'], response['resultMsg'] = check_body_request( rj, ('writer', 'title', 'content') )
            if response['resultCode'] != HTTPStatus.OK:
                raise Exception(response['resultMsg'])

            writer = rj['writer']
            title = rj['title']
            content= rj['content']            

            # 로그인 유저와 작성자 매칭 확인
            # if payload['userid'] and writer != payload['userid']:
            #     response["resultCode"] = HTTPStatus.INTERNAL_SERVER_ERROR
            #     raise Exception("does not match writer(userid)")

            # 쿼리 작성
            sql = '''INSERT INTO tb_board (writer, title, content, create_at, update_at) 
            VALUES(%s, %s, %s, %s, %s);'''
            dt = get_dt_now_to_str()
            is_connected, conn = db.connector()
            
            if is_connected == False:
                raise Exception(f"{conn[0]} : {conn[1]}")

            try:
                with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                    cursor.execute(sql, (writer, title, content, dt, dt))
                    conn.commit()
                    response['resultCode'] = HTTPStatus.OK
                    response['resultMsg'] = cursor.lastrowid
                    cursor.close()
                conn.close()
            except pymysql.err.MySQLError as ME:
                response['resultCode'] = HTTPStatus.FORBIDDEN
                raise Exception(f'{ME[0]} : {ME[1]}')            

        except Exception as ex:
            response['resultMsg'] = ex.args[0]
        
        if response['resultCode'] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR 
 
    
    @swag_from(written_list)
    def get(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg" : ''}

        try:
            # 토큰 확인
            response['resultCode'], payload = check_token(f_request.headers)
            if response['resultCode'] != HTTPStatus.OK:
                raise Exception(payload)

            # 쿼리 작성
            sql = '''SELECT id, writer, title content, create_at, update_at 
            FROM tb_board 
            WHERE writer=%s'''
            _flag, result = db.query(sql, payload['userid'])

            if _flag == False:
                response['resultCode'] = HTTPStatus.FORBIDDEN
                raise Exception(f'{result[0]} : {result[1]}')

            response['resultCode'] = HTTPStatus.OK
            response['resultMsg'] = result

        except Exception as ex:
            response['resultMsg'] = ex.args[0]

        if response['resultCode'] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR


    @swag_from(edit)
    def put(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg" : ''}

        try:
            # 토큰 확인
            response['resultCode'], payload = check_token(f_request.headers)
            if response['resultCode'] != HTTPStatus.OK:
                raise Exception(payload)

            rj = f_request.get_json()

            # request data 확인
            response['resultCode'], response['resultMsg'] = check_body_request( rj, ('id', 'title' 'writer') )
            if response['resultCode'] != HTTPStatus.OK:
                raise Exception(response['resultMsg'])

            id = rj['id']
            title = rj['title']
            writer = rj['writer']
            content = rj['content'] if rj['content'] else ''
            dt = get_dt_now_to_str()

            # 쿼리 작성
            sql = '''UPDATE tb_board 
            SET writer=%s, title=%s, content=%s, update_at=%s 
            WHERE id=%s;'''
            _flag, result = db.executer(sql, (writer, title, content, dt, int(id)) )

            if _flag == False:
                response['resultCode'] = HTTPStatus.FORBIDDEN
                raise Exception(f'{result[0]} : {result[1]}')

            if _flag and bool(result) == False:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception('No matching data')

            response['resultCode'] = HTTPStatus.OK
            response['resultMsg'] = 'Ok'
        
        except Exception as ex:
            response['resultMsg'] = ex.args[0]

        if response['resultCode'] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR