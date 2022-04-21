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
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg": '' }

    try:
        #토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

    except Exception as ex:
        response['resultMsg'] = ex.args[0]

    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR



