from http import HTTPStatus
from flask import jsonify, request as f_request
from flask_restful import Resource
from flasgger import Swagger, swag_from
import utils.database as database
from src.boards.board_method import board_post, board_get
from utils.function import get_dt_now_to_str, check_token


db = database.DBHandler()


class Board(Resource):
    @swag_from(board_post)
    def post(self):
        response = { "resultCode" : HTTPStatus.OK, "resultMsg" : '' }
        try:
            code, payload = check_token(f_request.headers)

            if code != HTTPStatus.OK:
                response['resultCode'] = code
                raise Exception(payload)

            rj = f_request.get_json()

            if rj is None:
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception("request data is empty")

            if rj['writer'] is None:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("Not found writer")

            if rj['content'] is None:
                response['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("Not found content")

            writer = rj['writer']
            content= rj['content']            

            if writer == "":
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception("writer is empty")

            if content == "":
                response["resultCode"] = HTTPStatus.NO_CONTENT
                raise Exception("content is empty")

            if payload['userid'] and writer != payload['userid']:
                response["resultCode"] = HTTPStatus.INTERNAL_SERVER_ERROR
                raise Exception("does not match writer(userid)")

            sql = '''INSERT INTO tb_board (writer, content, create_at, update_at) VALUES(%s, %s, %s, %s)'''
            dt = get_dt_now_to_str()
            _flag, result = db.executer(sql, (writer, content, dt, dt))

            if _flag:
                response['resultMsg'] = 'OK'
            else:
                response["resultCode"] = HTTPStatus.INTERNAL_SERVER_ERROR
                raise Exception(f"{result[0]} : {result[1]}")

        except Exception as ex:
            response['resultMsg'] = ex.args[0]
        
        if response['resultCode'] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR
    

    @swag_from(board_get)
    def get(self):
        response = { "resultCode" : HTTPStatus.OK, "resultMsg" : '' }
        try:
            code, payload = check_token(f_request.headers)

            if code != HTTPStatus.OK:
                response['resultCode'] = code
                raise Exception(payload)

            _flag, result = db.query('''SELECT id, writer, content, update_at FROM tb_board WHERE activate=1;''')

            if _flag == False:
                raise Exception(f"{result[0]} : {result[1]}")            

            response['resultMsg'] = result
        except Exception as ex:
            response['resultMsg'] = ex.args[0]

        if response['resultCode'] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR