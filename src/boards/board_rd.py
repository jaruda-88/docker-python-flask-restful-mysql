from http import HTTPStatus
from flask import Blueprint, jsonify, request as f_request
from flasgger import Swagger, swag_from
import databases as db
from utils.settings import DATABASE_CONFIG as con
from src.boards.board_methods import (
    delete_post,
    written_all_list,
    get_board_in_writer,
    get_board_in_title,
    get_board_in_content,
    written_paging
    )
from utils.function import (
    is_token,
    is_blank_str
    )


bp = Blueprint("board_rd", __name__, url_prefix="/api/board")
dbh = db.DBHandler(port=con['port'], user=con['user'], pw=con['pw'], database=con['db_name'], host=con['host'])


@bp.route('/delete/<id>', methods=['DELETE'])
@swag_from(delete_post, methods=['DELETE'])
def delete_board_in_id(id):
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

    try:
        # 토큰 확인
        try:
            is_token(f_request.headers)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.UNAUTHORIZED
            raise Exception(ex.args[0])

        if not id:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception("id is None")

        # db
        try:
            # 쿼리 작성
            sql = "DELETE FROM tb_board WHERE id={}".format(id)
            result = dbh.executer(sql=sql)

            if result == 0:
                response['resultCode'] = HTTPStatus.FORBIDDEN
                raise Exception('board_id does not match')
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            response['resultCode'] = HTTPStatus.OK
            response['resultMsg'] = "Ok"
            return jsonify(response)

    except Exception as ex:
        response['resultMsg'] = ex.args[0]
        return response, HTTPStatus.INTERNAL_SERVER_ERROR
        

@bp.route('/<id>', methods=['GET'])
@swag_from(written_all_list, methods=['GET'])
def get_board_in_id(id):
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }
    
    try:
        # 토큰 확인
        try:
            is_token(f_request.headers)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.UNAUTHORIZED
            raise Exception(ex.args[0])

        # request data 확인
        if not id:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('id is None')

        # db
        try:
            if int(id) == -1:
                sql = '''SELECT id, writer, title, content, create_at, update_at
                FROM tb_board
                ORDER BY update_at DESC;'''
                result = dbh.query(sql=sql)                
            else:
                sql = f'''SELECT id, writer, title, content, create_at, update_at            
                FROM tb_board
                WHERE id={id}
                ORDER BY update_at DESC;'''
                result = dbh.query(sql=sql, is_all=False)                
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            response['resultCode'] = HTTPStatus.OK
            response['resultMsg'] = result
            return jsonify(response)

    except Exception as ex:
        response['resultMsg'] = ex.args[0]
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('page/<num>/<limit>', methods=['GET'])
@swag_from(written_paging, methods=['GET'])
def get_board_page(num, limit):
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

    try:
        # 토큰 확인
        try:
            is_token(f_request.headers)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.UNAUTHORIZED
            raise Exception(ex.args[0])

        if not num:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('num is empty')
        
        if not limit:
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('limit is empty')

        # db
        try:
            pageNum = int(num)
            pageLimit = int(limit)

            # 쿼리 작성
            sql_list = [
                {
                    'sql': '''SELECT post.id, post.writer, post.title, post.update_at, COUNT(comment.id) as comment_count
                    FROM tb_board post
                        LEFT OUTER JOIN tb_board_comment comment
                        ON post.id=comment.board_id
                    GROUP BY post.id
                    ORDER BY post.update_at DESC
                    LIMIT %s, %s;''',
                    'value': ((pageNum * pageLimit), pageLimit),
                    'type': 'query',
                    'is_all': True
                },
                {
                    'sql': '''SELECT COUNT(id) AS count
                    FROM tb_board;''',
                    'type': 'query',
                    'is_all': False
                }
            ]
            # db 조회
            result = dbh.querys(sql_list=sql_list)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            response['resultCode'] = HTTPStatus.OK
            response['resultMsg'] = {'list': result[0], 'count' : result[1]['count']}
            return jsonify(response)

    except Exception as ex:
        response['resultMsg'] = ex.args[0]
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/writer', methods=['GET'])
@swag_from(get_board_in_writer, methods=['GET'])
def get_board_writer():
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

    try:
        # 토큰 확인
        try:
            is_token(f_request.headers)
        except Exception as ex:
            response['resultCode'] = HTTPStatus.UNAUTHORIZED
            raise Exception(ex.args[0])

        writer = f_request.args.get('writer', None)
        num = f_request.args.get('num', None)
        limit = f_request.args.get('limit', None)

        if is_blank_str(writer):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('writer is empty')
        
        if is_blank_str(num):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('num is empty')

        if is_blank_str(limit):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('limit is empty')

        # db
        try:
            pageNum = int(num)
            pageLimit = int(limit)

            # 쿼리 작성
            sql_list = [
                {
                    'sql': '''SELECT post.id, post.writer, post.title, post.update_at, COUNT(comment.id) as comment_count
                    FROM tb_board as post
                        LEFT OUTER JOIN tb_board_comment comment
                        ON post.id=comment.board_id
                    WHERE post.writer=%s
                    GROUP BY post.id
                    ORDER BY post.update_at DESC
                    LIMIT %s, %s;''',
                    'value': (writer, pageNum*pageLimit, pageLimit),
                    'type': 'query',
                    'is_all': True
                },
                {
                    'sql': f'''SELECT COUNT(id) AS count
                    FROM tb_board
                    WHERE writer='{writer}';''',
                    'type': 'query',
                    'is_all': False
                }
            ]
            # db 조회
            result = dbh.querys(sql_list=sql_list)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            response['resultCode'] = HTTPStatus.OK
            response['resultMsg'] = {'list': result[0], 'count' : result[1]['count']}
            return jsonify(response)
    
    except Exception as ex:
        response['resultMsg'] = ex.args[0]
        return response, HTTPStatus.INTERNAL_SERVER_ERROR
        

@bp.route('/title', methods=['GET'])
@swag_from(get_board_in_title, methods=['GET'])
def get_board_title():
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

    try:
        # 토큰 확인
        try:
            is_token(f_request.headers)
        except Exception as ex:
            raise Exception(ex.args[0])

        title = f_request.args.get('title', None)
        num = f_request.args.get('num', None)
        limit = f_request.args.get('limit', None)

        if is_blank_str(title):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('writer is empty')
        
        if is_blank_str(num):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('num is empty')

        if is_blank_str(limit):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('limit is empty')

        # db
        try:
            pageNum = int(num)
            pageLimit = int(limit)
            searchKeywork = f'%{title}%'

            # 쿼리 작성
            sql_list = [
                {
                    'sql': '''SELECT post.id, post.writer, post.title, post.update_at, COUNT(comment.id) AS comment_count
                    FROM tb_board post
                        LEFT OUTER JOIN tb_board_comment comment
                        ON post.id=comment.board_id
                    WHERE post.title LIKE %s
                    GROUP BY post.id
                    ORDER BY post.update_at DESC
                    LIMIT %s, %s;''',
                    'value': (searchKeywork, pageNum*pageLimit, pageLimit),
                    'type': 'query',
                    'is_all': True
                },
                {
                    'sql': f'''SELECT COUNT(id) AS count
                    FROM tb_board
                    WHERE title LIKE '{searchKeywork}';''',
                    'type': 'query',
                    'is_all': False
                }
            ]
            # db 조회
            result = dbh.querys(sql_list=sql_list)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            response['resultCode'] = HTTPStatus.OK
            response['resultMsg'] = {'list': result[0], 'count' : result[1]['count']}
            return jsonify(response)
    
    except Exception as ex:
        response['resultMsg'] = ex.args[0]
        return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/content', methods=['GET'])
@swag_from(get_board_in_content, methods=['GET'])
def get_board_content():
    response = { 'resultCode' : HTTPStatus.INTERNAL_SERVER_ERROR }

    try:
        # 토큰 확인
        try:
            is_token(f_request.headers)
        except Exception as ex:
            raise Exception(ex.args[0])

        content = f_request.args.get('content', None)
        num = f_request.args.get('num', None)
        limit = f_request.args.get('limit', None)

        if is_blank_str(content):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('writer is empty')
        
        if is_blank_str(num):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('num is empty')

        if is_blank_str(limit):
            response['resultCode'] = HTTPStatus.NO_CONTENT
            raise Exception('limit is empty')

        # db
        try:
            pageNum = int(num)
            pageLimit = int(limit)
            searchKeywork = f'%{content}%'
            
            # 쿼리 작성
            sql_list = [
                {
                    'sql': '''SELECT post.id, post.writer, post.title, post.update_at, COUNT(comment.id) as comment_count
                    FROM tb_board post
                        LEFT OUTER JOIN tb_board_comment comment
                        ON post.id=comment.board_id
                    WHERE post.content LIKE %s
                    GROUP BY post.id
                    ORDER BY post.update_at DESC
                    LIMIT %s, %s;''',
                    'value': (searchKeywork, pageNum*pageLimit, pageLimit),
                    'type': 'query',
                    'is_all': True
                },
                {
                    'sql': f'''SELECT COUNT(id) AS count
                    FROM tb_board
                    WHERE content LIKE '{searchKeywork}';''',
                    'type': 'query',
                    'is_all': False
                }
            ]
            # db 조회
            result = dbh.querys(sql_list=sql_list)
        except Exception as ex:
            raise Exception(ex.args[0])
        else:
            response['resultCode'] = HTTPStatus.OK
            response['resultMsg'] = {'list': result[0], 'count' : result[1]['count']}
            return jsonify(response)
        
    except Exception as ex:
        response['resultMsg'] = ex.args[0]
        return response, HTTPStatus.INTERNAL_SERVER_ERROR