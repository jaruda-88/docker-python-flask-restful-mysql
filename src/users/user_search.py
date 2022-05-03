from http import HTTPStatus
from flask import Blueprint, jsonify, request as f_request
from flasgger import Swagger, swag_from
import databases as db
from utils.settings import DATABASE_CONFIG as con
from src.users.user_methods import (
    user_get_in_id, 
    user_get_in_userid,
    user_get_in_username
    )
from utils.function import (
    is_token,
    is_blank_str
    )


bp = Blueprint("user_search", __name__, url_prefix="/api/user")
dbh = db.DBHandler(host=con['host'], user=con['user'], pw=con['pw'], database=con['db_name'], port=con['port'])


@bp.route('/<pk>', methods=['GET'])
@swag_from(user_get_in_id, methods=['GET'])
def get_userinfos_in_id(pk):
    response = { "resultCode": HTTPStatus.INTERNAL_SERVER_ERROR}
    
    try:
        # 토큰 확인
        try:
            is_token(f_request.headers)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.UNAUTHORIZED
            raise Exception(ex.args[0])

        if pk is None:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('pk is empyt')

        # db
        try:
            if int(pk) == -1:
                # 쿼리 작성
                sql = '''SELECT id, userid, username, connected_at 
                FROM tb_user
                WHERE activate=1;'''
                # db 조회
                result = dbh.query(sql=sql)
            else:
                # 쿼리 작성
                sql = '''SELECT id, userid, username, connected_at 
                FROM tb_user 
                WHERE activate=%s AND id=%s;'''
                # db 조회
                value = (1, int(pk))
                result = dbh.query(sql=sql, value=value, is_all=False)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.FORBIDDEN
            raise Exception(ex.args[0])
        else:
            response["resultCode"] = HTTPStatus.OK
            response['resultMsg'] = result
            return jsonify(response)

    except Exception as ex:
        response['resultMsg'] = ex.args[0] 
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/id/<userid>', methods=['GET'])
@swag_from(user_get_in_userid, methods=['GET'])
def get_userinfos_in_userid(userid):
    response = { "resultCode": HTTPStatus.INTERNAL_SERVER_ERROR }

    try:
        # 토큰 확인
        try:
            is_token(f_request.headers)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.UNAUTHORIZED
            raise Exception(ex.args[0])

        if is_blank_str(userid):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('userid is empyt')

        # db
        try:
            # 쿼리 작성
            sql = '''SELECT id, userid, username, connected_at 
            FROM tb_user 
            WHERE activate=%s AND userid=%s'''
            value = (1, userid)
            # db 조회
            result = dbh.query(sql=sql, value=value, is_all=False)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.FORBIDDEN
            raise Exception(ex.args[0])
        else:
            response["resultCode"] = HTTPStatus.OK
            response['resultMsg'] = result
            return jsonify(response)

    except Exception as ex:
        response['resultMsg'] = ex.args[0]
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/name/<name>', methods=['GET'])
@swag_from(user_get_in_username, methods=['GET'])
def get_userinfos_in_username(name):
    response = { "resultCode": HTTPStatus.INTERNAL_SERVER_ERROR}

    try:
        # 토큰 확인
        try:
            is_token(f_request.headers)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.UNAUTHORIZED
            raise Exception(ex.args[0])

        if is_blank_str(name):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('name is empty')

        # db
        try:
            sql = '''SELECT id, userid, username, connected_at 
            FROM tb_user 
            WHERE activate=%s AND username LIKE %s'''
            value = (1, "%{}%".format(name))
            result = dbh.query(sql=sql, value=value)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.FORBIDDEN
            raise Exception(ex.args[0])
        else:
            response["resultCode"] = HTTPStatus.OK
            response['resultMsg'] = result
            return jsonify(response)
    
    except Exception as ex:
        response['resultMsg'] = ex.args[0]
        return response, HTTPStatus.INTERNAL_SERVER_ERROR
    

