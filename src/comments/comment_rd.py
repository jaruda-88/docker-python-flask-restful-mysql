from flask import Blueprint, jsonify, request as f_request
from flasgger import Swagger, swag_from
from http import HTTPStatus
import utils.databases as db
from utils.settings import DATABASE_CONFIG as con
from utils.function import (
    is_token,
    is_blank_str
)
from src.comments.comment_methods import (
    comment_paging
)


bp = Blueprint("comment_rd", __name__, url_prefix="/api/board/comment")
dbh = db.DBHandler(host=con['host'], port=con['port'], user=con['user'], database=con['db_name'], pw=con['pw'])


@bp.route('/page', methods=['GET'])
@swag_from(comment_paging, methods=['GET'])
def get_board_comment_in_id():
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

    try:
        #토큰 확인
        try:
            is_token(f_request.headers)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.UNAUTHORIZED
            raise Exception(ex.args[0])

        num = f_request.args.get('num', None)
        limit = f_request.args.get('limit', None)
        board_id = f_request.args.get('board_id', None)

        if is_blank_str(num):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('num is empty')

        if is_blank_str(limit):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('limit is empty')

        if is_blank_str(board_id):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('board_id is empty')

        # db
        try:
            pageNum = int(num)
            pageLimit = int(limit)
            boardPk = int(board_id)
            sql_list = [
                {
                    'sql': '''SELECT comment.id, comment.content, comment.create_at, person.id AS user_id, person.userid AS writer
                    FROM tb_board_comment comment
                        INNER JOIN tb_user person
                        ON comment.user_id=person.id
                    WHERE comment.board_id=%s
                    ORDER BY comment.create_at DESC
                    LIMIT %s, %s;''',
                    'value': (boardPk, pageNum*pageLimit, pageLimit),
                    'type': 'query',
                    'all': True
                },
                {
                    'sql': f'''SELECT COUNT(id) AS count
                    FROM tb_board_comment
                    WHERE board_id={board_id};''',
                    'type': 'query',
                    'all': False
                }
            ]
            result = dbh.querys(sql_list=sql_list)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            response['resultCode'] = HTTPStatus.OK
            response['resultMsg'] = { 'list' : result[0], 'count' : result[1]['count'] }
            return jsonify(response)

    except Exception as ex:
        response['resultMsg'] = ex.args[0]
        return response, HTTPStatus.INTERNAL_SERVER_ERROR