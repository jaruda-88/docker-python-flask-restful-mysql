from flask import Blueprint
from http import HTTPStatus
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database
from src.users.user_methods import (
    user_get_in_id, 
    user_get_in_userid,
    user_get_in_username
    )
from utils.function import (
    check_token,
    is_blank_str
    )


bp = Blueprint("user_search", __name__, url_prefix="/api/user")
db = database.DBHandler()


@bp.route('/<pk>', methods=['GET'])
@swag_from(user_get_in_id, methods=['GET'])
def get_userinfos_in_id(pk):
    response = { "resultCode": HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg": '' }
    
    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        if pk is None:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('pk is empyt')

        # 쿼리 작성
        if int(pk) == -1:
            sql = '''SELECT id, userid, username, connected_at 
            FROM tb_user;'''
        else:
            sql = f'''SELECT id, userid, username, connected_at 
            FROM tb_user 
            WHERE activate=1 AND id={int(pk)};'''
        _flag, result = db.query(sql)

        # db 조회 실패
        if _flag == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f"{result[0] : result[1]}")

        response["resultCode"] = HTTPStatus.OK
        response['resultMsg'] = result

    except Exception as ex:
        response['resultMsg'] = ex.args[0] 

    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/id/<userid>', methods=['GET'])
@swag_from(user_get_in_userid, methods=['GET'])
def get_userinfos_in_userid(userid):
    response = { "resultCode": HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg": '' }

    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        if is_blank_str(userid):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('userid is empyt')

        # 쿼리 작성
        sql = '''SELECT id, userid, username, connected_at 
        FROM tb_user 
        WHERE activate=1 AND userid=%s'''
        _flag, result = db.query(sql, userid)

        # db 조회 실패
        if _flag == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f"{result[0]} : {result[1]}")

        response["resultCode"] = HTTPStatus.OK
        response['resultMsg'] = result

    except Exception as ex:
        response['resultMsg'] = ex.args[0]

    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/name/<name>', methods=['GET'])
@swag_from(user_get_in_username, methods=['GET'])
def get_userinfos_in_username(name):
    response = { "resultCode": HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg": '' }

    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        if is_blank_str(name):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('name is empty')

        # 쿼리 작성
        sql = '''SELECT id, userid, username, connected_at 
        FROM tb_user 
        WHERE activate=1 AND username LIKE %s'''
        search = "%{}%".format(name)
        _flag, result = db.query(sql, search)

        # db 조회 실패
        if _flag == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f"{result[0]} : {result[1]}")

        response["resultCode"] = HTTPStatus.OK
        response['resultMsg'] = result

    
    except Exception as ex:
        response['resultMsg'] = ex.args[0]

    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR
    

