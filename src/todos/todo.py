from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database
from src.todos.todo_view import *

db = utils.database.DBHandler()

"""import requests
import json
import os
import sys"""

class Todo(Resource):
    @swag_from(todo_get)
    def get(self):
        #result = { "resultCode" : "", "resultMsg" : "" }

        try:
            pk = f_request.args.get('todo_id')

            print(pk)

            if pk == "":
                raise Exception('value empty')

            if int(pk) == -1:
                query = '''SELECT * FROM tb_todo;'''
            else:
                query = f'''SELECT * FROM tb_todo where id={int(pk)};'''
            
            _flag, data = db.query(query)

            print(data)

            if _flag == False:
                raise Exception(f"{data[0]} : {data[1]}")            
            
            return jsonify(data)
            #result["resultCode"] = HTTPStatus.OK
            #result["resultMsg"] = data

        except Exception as ex:
            #result["resultCode"] = HTTPStatus.INTERNAL_SERVER_ERROR
            #result["resultMsg"] = ex.args[0]
            return jsonify(ex.args[0])
