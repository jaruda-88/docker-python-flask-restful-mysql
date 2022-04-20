from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database
from utils.function import(
    check_body_request,
    check_token,
    get_dt_now_to_str
)

db = database.DBHandler()

class Comment(Resource):
    @swag_from('comment.yml', validation=True)
    def post(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg" : '' }

        try:
            response['resultCode'], payload = check_token(f_request.headers)

            if response['resultCode'] != HTTPStatus.OK:
                raise Exception(payload)

            rj = f_request.get_json()

            response['resultCode'], response['resultMsg'] = check_body_request (rj, ('writer', 'content') )

            boardId = int(rj['board_id']) if rj['board_id'] else -100
            if boardId == -100:
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('board_id is empty')
            
            writer = rj['writer']
            content = rj['content']
            dt = get_dt_now_to_str()

            # 쿼리 작성
            sql = '''INSERT INTO tb_board_comment (board_id, writer, content, create_at)
            SELECT %s,%s,%s,%s;'''
            # db 조회
            _flag, result = db.executer(sql, (boardId, writer, content, dt))

            # db 조회 실패
            if _flag == False:
                response["resultCode"] = HTTPStatus.NOT_FOUND
                raise Exception(f"{result[0]} : {result[1]}")
            
            if _flag and bool(result) == False:
                response["resultCode"] = HTTPStatus.FORBIDDEN
                raise Exception('board_id error')

            response["resultCode"] = HTTPStatus.OK
            response["resultMsg"] = 'Ok'

        except Exception as ex:
            response['resultMsg'] = ex.args[0]

        if response['resultCode'] == HTTPStatus.OK:
            return jsonify(response)
        else:
            return response, HTTPStatus.INTERNAL_SERVER_ERROR
