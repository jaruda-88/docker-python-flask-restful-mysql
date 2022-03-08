from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database
from src.todos.todo_view import *

db = database.DBHandler()

class Todo(Resource):
    @swag_from(todo_post, validation=True)
    def post(self):

        try:
            rj = f_request.get_json()

            task = rj['task']
            
            if task == "":
                raise Exception('todo is empty')

            query = '''INSERT INTO tb_todo (todo) VALUES(%s);'''

            # db.executer(query, (value, value, value))
            _flag, result = db.executer(query, task)

            if _flag == False:
                raise Exception(f"{result[0]} : {result[1]}")    

            return jsonify('OK')
        except Exception as ex:
            return jsonify(ex.args[0])


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
            
            _flag, result = db.query(query)

            if _flag == False:
                raise Exception(f"{result[0]} : {result[1]}")            
            
            return jsonify(result)
            #result["resultCode"] = HTTPStatus.OK
            #result["resultMsg"] = data

        except Exception as ex:
            #result["resultCode"] = HTTPStatus.INTERNAL_SERVER_ERROR
            #result["resultMsg"] = ex.args[0]
            return jsonify(ex.args[0])
