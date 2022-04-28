from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.databases as db
from utils.settings import DATABASE_CONFIG as con
from utils.function import(
    is_token,
    get_dt_now_to_str,
    is_blank_str
)


dbh = db.DBHandler(host=con['host'], port=con['port'], user=con['user'], database=con['db_name'], pw=con['pw'])


class Comment(Resource):
    @swag_from('comment.yml', validation=True)
    def post(self):
        response = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR }

        try:
            # token 확인
            try:
                is_token(f_request.headers)
            except Exception as ex:
                response['resultCode'] = HTTPStatus.UNAUTHORIZED
                raise Exception(ex.args[0])

            rj = f_request.get_json()

            userId = rj.get('user_id', None)
            boardId = rj.get('board_id', None)
            content = rj.get('content', None)

            if not userId:
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('user_id is empty')

            if not boardId:
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('board_id is empty')

            if is_blank_str(content):
                response['resultCode'] = HTTPStatus.NO_CONTENT
                raise Exception('conten is empty')

            # db
            try:
                # 쿼리 작성
                sql = '''INSERT INTO tb_board_comment (user_id, board_id, content, create_at)
                SELECT %s,%s,%s,%s;'''
                dt = get_dt_now_to_str()
                value = (userId, boardId, content, dt)
                # db 조회
                result = dbh.executer(sql=sql, value=value, last_id=True)
                
                if result == 0:
                    response['resultCode'] = HTTPStatus.FORBIDDEN
                    raise Exception('post fail')
            except Exception as ex:
                raise Exception(ex.args[0])
            else:
                response["resultCode"] = HTTPStatus.OK
                response["resultMsg"] = 'Ok'
                return jsonify(response)

        except Exception as ex:
            response['resultMsg'] = ex.args[0]
            return response, HTTPStatus.INTERNAL_SERVER_ERROR
            
