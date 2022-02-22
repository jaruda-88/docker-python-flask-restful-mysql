from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from


"""import requests
import json
import os
import sys"""

class Todo(Resource):

    @swag_from('todo.yml', validation=True)
    def post(self):
        return "test"
        """result = {  "resultCode" :  "", "resultMsg" : "" }

        try:            
            rj = f_request.get_json()

            phonenumber = rj['phonenumber']
            req_id = rj['req_id']

            if phonenumber == "":
                raise Exception('phonenumber is empty') 
            if req_id == "":
                raise Exception('req_id is empty') 

            result["resultCode"] = HTTPStatus.OK
            result["resultMsg"] = "Ok."

            return jsonify(result)

        except Exception as ex:

            result["resultCode"] = HTTPStatus.INTERNAL_SERVER_ERROR
            result["resultMsg"] = ex.args[0]

            return jsonify(result)"""
