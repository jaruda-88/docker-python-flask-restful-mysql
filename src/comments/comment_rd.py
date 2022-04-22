from flask import Blueprint, jsonify, request as f_request
from flasgger import Swagger, swag_from
from http import HTTPStatus
import utils.database as database
from utils.function import (
    check_token,
    is_blank_str
)
from src.comments.comment_methods import (
    comment_paging
)


bp = Blueprint("comment_rd", __name__, url_prefix="/api/board/comment")
db = database.DBHandler()


@bp.route('/page', methods=['GET'])
@swag_from(comment_paging, methods=['GET'])
def get_board_comment_in_id():
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

    try:
        #토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        num = f_request.args.get('num')
        limit = f_request.args.get('limit')
        board_id = f_request.args.get('board_id')

        if is_blank_str(num):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('num is empty')

        if is_blank_str(limit):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('limit is empty')

        if is_blank_str(board_id):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('board_id is empty')

        pageNum = int(num)
        pageLimit = int(limit)
        boardPk = int(board_id)

        # 쿼리 작성
        sql_list = ['''SELECT comment.id, comment.content, comment.create_at, person.id AS user_id, person.userid AS writer
        FROM tb_board_comment comment
            INNER JOIN tb_user person
            ON comment.user_id=person.id
        WHERE comment.board_id=%s
        ORDER BY comment.create_at DESC
        LIMIT %s, %s;''',
        '''SELECT COUNT(id) AS count
        FROM tb_board_comment
        WHERE board_id=%s;''']
        val_list = [ (boardPk, pageNum*pageLimit, pageLimit), board_id ]
        # db 조회
        _flag, result = db.querys(query_list=sql_list, value_list=val_list)

        # db 조회 실패
        if _flag == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f'{result[0]} : {result[1]}')

        response['resultCode'] = HTTPStatus.OK
        response['resultMsg'] = { 'list' : result[0], 'count' : result[1] }

    except Exception as ex:
        response['resultMsg'] = ex.args[0]

    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR



