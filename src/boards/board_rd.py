from flask import Blueprint
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
from http import HTTPStatus
import utils.database as database
from src.boards.board_methods import (
    delete_post
)
from utils.function import check_token


bp = Blueprint("board_rd", __name__, url_prefix="/api/board")
db = database.DBHandler()


@bp.route('/delete/<id>', methods=['DELETE'])
@swag_from(delete_post, methods=['DELETE'])
def delete_board_in_id(id):
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg" : 'Ok' }

    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        if id is None:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception("id is None")

        if int(id) <= 0:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception("No value id")

        # 쿼리 작성
        sql = f'''DELETE FROM tb_board WHERE id={int(id)}'''
        _flag, result = db.executer(sql)

        if _flag == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f'{result[0]} : {result[1]}')
        
        # insert 성공 시 1
        # insert 실패 시 0
        if _flag and bool(result) == False:
            response['resultCode'] = HTTPStatus.FORBIDDEN
            raise Exception('board_id does not match')

        response['resultCode'] = HTTPStatus.OK
        response['resultMsg'] = "Ok"

    except Exception as ex:
        response['resultMsg'] = ex.args[0]

    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR