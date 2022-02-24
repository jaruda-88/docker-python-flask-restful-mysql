from flask_restful import Resource
from flask import jsonify, request as f_request
from flasgger import Swagger, swag_from
import utils.database

db = utils.database.DBHandler()

"""import requests
import json
import os
import sys"""


class Todo(Resource):
    @swag_from('todo.yml', validation=True)
    def post(self):
        _flag, data = db.query('''SELECT * FROM tb_task;''')
        return jsonify({"dd":data})
