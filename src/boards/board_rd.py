from http import HTTPStatus
from flask import Blueprint, jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.databases as dbs
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
dbh = dbs.DBHandler(port=con['port'], user=con['user'], pw=con['pw'], database=con['db_name'], host=con['host'])


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

        if id is None:
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
    pass
    # try:
    #     # 토큰 확인
    #     response['resultCode'], payload = check_token(f_request.headers)
    #     if response['resultCode'] != HTTPStatus.OK:
    #         raise Exception(payload)

    #     # request data 확인
    #     if id is None:
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('id is None')

    #     # 쿼리 작성
    #     if int(id) == -1:
    #         sql = '''SELECT id, writer, title, content, create_at, update_at
    #         FROM tb_board
    #         ORDER BY update_at DESC;'''
    #     else:
    #         sql = f'''SELECT id, writer, title, content, create_at, update_at            
    #         FROM tb_board
    #         WHERE id={id}
    #         ORDER BY update_at DESC;'''
    #     _flag, result = db.query(sql)

    #     if _flag == False:
    #         response['resultCode'] = HTTPStatus.NOT_FOUND
    #         raise Exception(f'{result[0]} : {result[1]}')

    #     response['resultCode'] = HTTPStatus.OK
    #     response['resultMsg'] = result

    # except Exception as ex:
    #     response['resultMsg'] = ex.args[0]

    # if response['resultCode'] == HTTPStatus.OK:
    #     return jsonify(response)
    # else:
    #     return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('page/<num>/<limit>', methods=['GET'])
@swag_from(written_paging, methods=['GET'])
def get_board_page(num, limit):
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }
    pass
    # try:
    #     # 토큰 확인
    #     response['resultCode'], payload = check_token(f_request.headers)
    #     if response['resultCode'] != HTTPStatus.OK:
    #         raise Exception(payload)

    #     if num is None:
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('num is empty')
        
    #     if limit is None:
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('limit is empty')

    #     pageNum = int(num)
    #     pageLimit = int(limit)

    #     # 쿼리 작성
    #     sql_list = ['''SELECT post.id, post.writer, post.title, post.update_at, COUNT(comment.id) as comment_count
    #     FROM tb_board post
    #         LEFT OUTER JOIN tb_board_comment comment
    #         ON post.id=comment.board_id
    #     GROUP BY post.id
    #     ORDER BY post.update_at DESC
    #     LIMIT %s, %s;
    #     ''',
    #     '''SELECT COUNT(id) AS count
    #     FROM tb_board;''']
    #     value_list = [((pageNum * pageLimit), pageLimit), '']

    #     _flag, result = db.querys(query_list=sql_list, value_list=value_list)

    #     if _flag == False:
    #         response['resultCode'] = HTTPStatus.FORBIDDEN
    #         raise Exception(f'{result[0]} : {result[1]}')

    #     response['resultCode'] = HTTPStatus.OK
    #     response['resultMsg'] = {'list': result[0], 'count' : result[1]}

    # except Exception as ex:
    #     response['resultMsg'] = ex.args[0]

    # if response['resultCode'] == HTTPStatus.OK:
    #     return jsonify(response)
    # else:
    #     return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/writer', methods=['GET'])
@swag_from(get_board_in_writer, methods=['GET'])
def get_board_writer():
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }
    pass
    # try:
    #     # 토큰 확인
    #     response['resultCode'], payload = check_token(f_request.headers)
    #     if response['resultCode'] != HTTPStatus.OK:
    #         raise Exception(payload)

    #     writer = f_request.args.get('writer')
    #     num = f_request.args.get('num')
    #     limit = f_request.args.get('limit')

    #     if is_blank_str(writer):
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('writer is empty')
        
    #     if is_blank_str(num):
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('num is empty')

    #     if is_blank_str(limit):
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('limit is empty')

    #     pageNum = int(num)
    #     pageLimit = int(limit)
        
    #     # 쿼리 작성
    #     sql_list = ['''SELECT post.id, post.writer, post.title, post.update_at, COUNT(comment.id) as comment_count
    #     FROM tb_board as post
    #         LEFT OUTER JOIN tb_board_comment comment
    #         ON post.id=comment.board_id
    #     WHERE post.writer=%s
    #     GROUP BY post.id
    #     ORDER BY post.update_at DESC
    #     LIMIT %s, %s;''',
    #     '''SELECT COUNT(id) AS count
    #     FROM tb_board
    #     WHERE writer=%s;'''] 
    #     value_list = [(writer, pageNum*pageLimit, pageLimit), writer]
    #     # db 조회
    #     _flag, result = db.querys(query_list=sql_list, value_list=value_list)

    #     if _flag == False:
    #         response['resultCode'] = HTTPStatus.NOT_FOUND
    #         raise Exception(f'{result[0]} : {result[1]}')

    #     response['resultCode'] = HTTPStatus.OK
    #     response['resultMsg'] = {'list': result[0], 'count' : result[1]}
    
    # except Exception as ex:
    #     response['resultMsg'] = ex.args[0]
    
    # if response['resultCode'] == HTTPStatus.OK:
    #     return jsonify(response)
    # else:
    #     return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/title', methods=['GET'])
@swag_from(get_board_in_title, methods=['GET'])
def get_board_title():
    response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }
    pass
    # try:
    #     # 토큰 확인
    #     response['resultCode'], payload = check_token(f_request.headers)
    #     if response['resultCode'] != HTTPStatus.OK:
    #         raise Exception(payload)

    #     title = f_request.args.get('title')
    #     num = f_request.args.get('num')
    #     limit = f_request.args.get('limit')

    #     if is_blank_str(title):
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('writer is empty')
        
    #     if is_blank_str(num):
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('num is empty')

    #     if is_blank_str(limit):
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('limit is empty')

    #     pageNum = int(num)
    #     pageLimit = int(limit)
    #     searchKeywork = f'%{title}%'
        
    #     # 쿼리 작성
    #     sql_list = ['''SELECT post.id, post.writer, post.title, post.update_at, COUNT(comment.id) AS comment_count
    #     FROM tb_board post
    #         LEFT OUTER JOIN tb_board_comment comment
    #         ON post.id=comment.board_id
    #     WHERE post.title LIKE %s
    #     GROUP BY post.id
    #     ORDER BY post.update_at DESC
    #     LIMIT %s, %s;''',
    #     '''SELECT COUNT(id) AS count
    #     FROM tb_board 
    #     WHERE title LIKE %s;''']
    #     value_list = [ (searchKeywork, pageNum*pageLimit, pageLimit), searchKeywork ]
    #     # db 조회
    #     _flag, result = db.querys(query_list=sql_list, value_list=value_list)

    #     if _flag == False:
    #         response['resultCode'] = HTTPStatus.NOT_FOUND
    #         raise Exception(f'{result[0]} : {result[1]}')
        
    #     response['resultCode'] = HTTPStatus.OK
    #     response['resultMsg'] = {'list': result[0], 'count' : result[1]}
    
    # except Exception as ex:
    #     response['resultMsg'] = ex.args[0]

    # if response['resultCode'] == HTTPStatus.OK:
    #     return jsonify(response)
    # else:
    #     return response, HTTPStatus.INTERNAL_SERVER_ERROR


@bp.route('/content', methods=['GET'])
@swag_from(get_board_in_content, methods=['GET'])
def get_board_content():
    response = { 'resultCode' : HTTPStatus.INTERNAL_SERVER_ERROR }
    pass
    # try:
    #     # 토큰 확인
    #     response['resultCode'], payload = check_token(f_request.headers)
    #     if response['resultCode'] != HTTPStatus.OK:
    #         raise Exception(payload)

    #     content = f_request.args.get('content')
    #     num = f_request.args.get('num')
    #     limit = f_request.args.get('limit')

    #     if is_blank_str(content):
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('writer is empty')
        
    #     if is_blank_str(num):
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('num is empty')

    #     if is_blank_str(limit):
    #         response['resultCode'] = HTTPStatus.NO_CONTENT
    #         raise Exception('limit is empty')

    #     pageNum = int(num)
    #     pageLimit = int(limit)
    #     searchKeywork = f'%{content}%'
        
    #     # 쿼리 작성
    #     sql_list = ['''SELECT post.id, post.writer, post.title, post.update_at, COUNT(comment.id) as comment_count
    #     FROM tb_board post
    #         LEFT OUTER JOIN tb_board_comment comment
    #         ON post.id=comment.board_id
    #     WHERE post.content LIKE %s
    #     GROUP BY post.id
    #     ORDER BY post.update_at DESC
    #     LIMIT %s, %s;''',
    #     '''SELECT COUNT(id) AS count 
    #     FROM tb_board 
    #     WHERE content LIKE %s;'''] 
    #     value_list = [(searchKeywork, pageNum*pageLimit, pageLimit), searchKeywork]
    #     _flag, result = db.querys(query_list=sql_list, value_list=value_list)

    #     if _flag == False:
    #         response['resultCode'] = HTTPStatus.NOT_FOUND
    #         raise Exception(f'{result[0]} : {result[1]}')
        
    #     response['resultCode'] = HTTPStatus.OK
    #     response['resultMsg'] = {'list': result[0], 'count' : result[1]}
        
    # except Exception as ex:
    #     response['resultMsg'] = ex.args[0]

    # if response['resultCode'] == HTTPStatus.OK:
    #     return jsonify(response)
    # else:
    #     return response, HTTPStatus.INTERNAL_SERVER_ERROR