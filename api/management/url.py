from flask_restplus import Resource
from api import management_ns


ns = management_ns


@ns.route('/test')
class test(Resource):
    def get(self, id):
        ''' dddd '''
        return "dddd"