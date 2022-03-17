from http import HTTPStatus
from math import fabs
from unittest import result
from flask_restful import Resource
from flask import jsonify, request as f_request
from itsdangerous import json
from flasgger import Swagger, swag_from
import utils.database as database
import hashlib
import datetime


db = database.DBHandler()


class User(Resource):
    @swag_from('registration_user.yml', validation=True)
    def post(self):
        try:
            rj = f_request.get_json()

            userid = rj['userid']
            usernm = rj['username']
            pw = rj['pw']

            if userid == "":
                raise Exception('userid is empty')
            
            if pw == "":
                raise Exception('password is empty')

            pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

            _flag, result = db.executer('''INSERT INTO tb_user (userid, username, pw, create_at) 
            SELECT %s,%s,%s,%s 
            FROM 
            DUAL WHERE NOT EXISTS(SELECT * FROM tb_user WHERE userid=%s);''', 
            (userid, usernm, pw_hash, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), userid))

            if _flag == False:
                raise Exception(f"{result[0]} : {result[1]}")

            if type(result) is int and bool(result) == False: 
                raise Exception('userid already registered')
                
            resp = { "resultCode" : HTTPStatus.OK, "resultMsg" : 'success' }
                
        except Exception as ex:
            resp = { "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, "resultMsg" : ex.args[0] }

        return jsonify(resp)