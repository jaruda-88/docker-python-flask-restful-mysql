from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database
from src.users.user_views import user_get
from utils.function import decode_token


db = database.DBHandler()


class User(Resource):
    @swag_from(user_get)
    def get(self):
        resp = { "resultCode" : HTTPStatus.OK, "resultMsg" : '' }
        try:
            auth = f_request.headers.get('Authorization')

            if auth is None:
                resp['resultCode'] = HTTPStatus.NON_AUTHORITATIVE_INFORMATION
                raise Exception("None token")

            payload = decode_token(auth)

            if payload is None:
                resp['resultCode'] = HTTPStatus.NOT_ACCEPTABLE
                raise Exception("Token Expiration")

            _flag, result = db.query('''SELECT create_at, id, userid, username FROM tb_user WHERE userid=%s''', payload['userid'])

            if _flag == False:
                resp['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception(f"{result[0]} : {result[1]}")

            if _flag and result is None or len(result) <= 0:
                resp['resultCode'] = HTTPStatus.NOT_FOUND
                raise Exception("not user data")

            resp["resultMsg"] = result[0]
                
        except Exception as ex:
            resp["resultMsg"] = ex.args[0]

        if resp["resultCode"] == HTTPStatus.OK:
            return jsonify(resp)
        else:
            return resp, HTTPStatus.INTERNAL_SERVER_ERROR