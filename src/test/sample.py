from http import HTTPStatus
from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database as database

db = database.DBHandler()

class sample(Resource):
    @swag_from('sample.yml')
    def get(self):
        try:
            query = '''SELECT * FROM tb_todo;'''

            _flag, result = db.query(query)

            if _flag:
                result = { 
                    "resultCode" : HTTPStatus.OK, 
                    "resultMsg" : result
                    }
            else:
                raise Exception(f"{result[0]} : {result[1]}")

        except Exception as ex:
            result = { 
                    "resultCode" : HTTPStatus.INTERNAL_SERVER_ERROR, 
                    "resultMsg" : ex.args[0]
                }
                
        return jsonify(result)
