from flask import Blueprint
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
from http import HTTPStatus
import utils.database as database
from src.boards.board_methods import (
    delete_post,
    written_all_list,
    get_board_in_writer,
    get_board_in_title,
    get_board_in_content,
    get_board_search
    )
from utils.function import (
    check_token,
    is_blank_str
    )


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


@bp.route('/<id>', methods=['GET'])
@swag_from(written_all_list, methods=['GET'])
def get_board_in_id(id):
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg" : '' }

    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        # request data 확인
        if id is None:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('id is None')

        # 쿼리 작성
        if int(id) == -1:
            sql = '''SELECT id, writer, title, content, update_at
            FROM tb_board
            ORDER BY update_at DESC;'''
        else:
            sql = f'''SELECT id, writer, title, content, update_at 
            FROM tb_board;
            WHERE id={int(id)}
            ORDER BY update_at DESC;'''
        _flag, result = db.query(sql)

        if _flag == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f'{result[0]} : {result[1]}')

        response['resultCode'] = HTTPStatus.OK
        response['resultMsg'] = result

    except Exception as ex:
        response['resultMsg'] = ex.args[0]

    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/writer/<writer>', methods=['GET'])
@swag_from(get_board_in_writer, methods=['GET'])
def get_board_writer(writer):
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg": '' }
    
    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        # request data 확인
        if is_blank_str(writer):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('value is empty')

        # 쿼리 작성
        sql = '''SELECT id, writer, title, content, update_at
        FROM tb_board
        WHERE writer=%s
        ORDER BY update_at DESC;'''
        _flag, result = db.query(sql, writer)

        if _flag == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f'{result[0]} : {result[1]}')

        response['resultCode'] = HTTPStatus.OK
        response['resultMsg'] = result
    
    except Exception as ex:
        response['resultMsg'] = ex.args[0]
    
    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/title/<title>', methods=['GET'])
@swag_from(get_board_in_title, methods=['GET'])
def get_board_title(title):
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg": '' }

    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        # request data 확인
        if is_blank_str(title):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('title is empyt')
        
        # 쿼리 작성
        sql = '''SELECT id, writer, title, content, update_at
        FROM tb_board
        WHERE title LIKE %s
        ORDER BY update_at DESC;'''
        _flag, result = db.query(sql, f'%{title}%')

        if _flag == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f'{result[0]} : {result[1]}')
        
        response['resultCode'] = HTTPStatus.OK
        response['resultMsg'] = result
    
    except Exception as ex:
        response['resultMsg'] = ex.args[0]

    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/content/<content>', methods=['GET'])
@swag_from(get_board_in_content, methods=['GET'])
def get_board_content(content):
    response = { 'resultCode' : HTTPStatus.INTERNAL_SERVER_ERROR, 'resultMsg' : '' }

    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        # request data 확인
        if is_blank_str(content):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('content is empty')

        # 쿼리 작성
        sql = '''SELECT id, writer, title, content, update_at
        FROM tb_board 
        WHERE content LIKE %s
        ORDER BY update_at DESC;'''
        _flag, result = db.query(sql, f'%{content}%')

        if _flag == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f'{result[0]} : {result[1]}')
        
        response['resultCode'] = HTTPStatus.OK
        response['resultMsg'] = result
        
    except Exception as ex:
        response['resultMsg'] = ex.args[0]

    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/search/<contents>', methods=['GET'])
@swag_from(get_board_search, methods=['GET'])
def get_board_in_title_and_content(contents):
    response = { 'resultCode' : HTTPStatus.INTERNAL_SERVER_ERROR, 'resultMsg' : '' }

    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        # request data 확인
        if is_blank_str(contents):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('contents is empty')
        
        # 쿼리 작성
        sql = '''SELECT id, writer, title, content, update_at
        FROM tb_board
        WHERE title LIKE %s OR content LIKE %s
        ORDER BY update_at DESC;'''
        keyword = f'%{contents}%'
        _flag, result = db.query(sql, (keyword, keyword))

        if _flag == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f'{result[0]} : {result[1]}')

        response['resultCode'] = HTTPStatus.OK
        response['resultMsg'] = result
    
    except Exception as ex:
        response['resultMsg'] = ex.args[0]

    if response['resultCode'] == HTTPStatus.OK:
        return jsonify(response)
    else:
        return response, HTTPStatus.INTERNAL_SERVER_ERROR