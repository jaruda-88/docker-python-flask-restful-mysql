import http
from flask import Blueprint
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
from http import HTTPStatus
import utils.database as database
import pymysql
import sys
from src.boards.board_methods import (
    delete_post,
    written_all_list,
    get_board_in_writer,
    get_board_in_title,
    get_board_in_content,
    written_paging
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
            sql = '''SELECT id, writer, title, content, create_at, update_at
            FROM tb_board
            ORDER BY update_at DESC;'''
        else:
            sql = f'''SELECT id, writer, title, content, create_at, update_at 
            FROM tb_board
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


@bp.route('page/<num>/<limit>', methods=['GET'])
@swag_from(written_paging, methods=['GET'])
def get_board_page(num, limit):
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        if num is None:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('num is empty')
        
        if limit is None:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('limit is empty')

        pageNum = int(num)
        pageLimit = int(limit)

        # 쿼리 작성
        sql_list = '''SELECT id, writer, title, update_at
        FROM tb_board
        ORDER BY update_at DESC
        LIMIT %s, %s;
        '''
        sql_count = '''SELECT COUNT(*) FROM tb_board;'''
        
        is_connected, conn = db.connector()

        if is_connected == False:
            response['resultCode'] = HTTPStatus.NOT_FOUND
            raise Exception(f'{conn[0]} : {conn[1]}')

        try:
            with conn.cursor(pymysql.cursors.DictCursor) as cursor:
                # limit 검색
                cursor.execute(sql_list, ((pageNum * pageLimit), pageLimit))
                list = cursor.fetchall()

                # table count all
                cursor.execute(sql_count)
                count = cursor.fetchall()
                
                response['resultCode'] = HTTPStatus.OK
                response['resultMsg'] = {'count': int(count[0]['COUNT(*)']), 'list' : list} 
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


@bp.route('/writer', methods=['GET'])
@swag_from(get_board_in_writer, methods=['GET'])
def get_board_writer():
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg": '' }
    
    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        writer = f_request.args.get('writer')
        pageNum = f_request.args.get('num')
        pagelimit = f_request.args.get('limit')

        if is_blank_str(writer):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('writer is empty')
        
        if not pageNum:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('num is empty')

        if not pagelimit:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('limit is empty')
        
        # 쿼리 작성
        sql_list = '''SELECT id, writer, title, update_at
        FROM tb_board
        WHERE writer=%s
        ORDER BY update_at DESC
        LIMIT %s, %s;'''
        sql_count = '''SELECT COUNT(*) FROM 
        tb_board 
        WHERE writer=%s;'''
        _flag, result = db.query_paging(\
            query_list=sql_list, 
            query_count=sql_count, 
            value=(writer, (int(pageNum)*int(pagelimit)), int(pagelimit))
        )

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


@bp.route('/title', methods=['GET'])
@swag_from(get_board_in_title, methods=['GET'])
def get_board_title():
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg": '' }

    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        title = f_request.args.get('title')
        pageNum = f_request.args.get('num')
        pagelimit = f_request.args.get('limit')

        if is_blank_str(title):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('writer is empty')
        
        if not pageNum:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('num is empty')

        if not pagelimit:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('limit is empty')
        
        # 쿼리 작성
        sql_list = '''SELECT id, writer, title, update_at
        FROM tb_board
        WHERE title LIKE %s
        ORDER BY update_at DESC
        LIMIT %s, %s;'''
        sql_count = '''SELECT COUNT(*) FROM 
        tb_board 
        WHERE title LIKE %s;'''
        _flag, result = db.query_paging(\
            query_list=sql_list, 
            query_count=sql_count, 
            value=(f'%{title}%', (int(pageNum)*int(pagelimit)), int(pagelimit))
        )

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


@bp.route('/content', methods=['GET'])
@swag_from(get_board_in_content, methods=['GET'])
def get_board_content():
    response = { 'resultCode' : HTTPStatus.INTERNAL_SERVER_ERROR, 'resultMsg' : '' }

    try:
        # 토큰 확인
        response['resultCode'], payload = check_token(f_request.headers)
        if response['resultCode'] != HTTPStatus.OK:
            raise Exception(payload)

        content = f_request.args.get('content')
        pageNum = f_request.args.get('num')
        pagelimit = f_request.args.get('limit')

        if is_blank_str(content):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('writer is empty')
        
        if not pageNum:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('num is empty')

        if not pagelimit:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('limit is empty')
        
        # 쿼리 작성
        sql_list = '''SELECT id, writer, title, update_at
        FROM tb_board
        WHERE content LIKE %s
        ORDER BY update_at DESC
        LIMIT %s, %s;'''
        sql_count = '''SELECT COUNT(*) FROM 
        tb_board 
        WHERE content LIKE %s;'''
        _flag, result = db.query_paging(\
            query_list=sql_list, 
            query_count=sql_count, 
            value=(f'%{content}%', (int(pageNum)*int(pagelimit)), int(pagelimit))
        )

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