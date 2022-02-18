# http 요청 처리.


from flask_restx import Resource
from .dto import ManagementDto
import utils.database


api = ManagementDto.api
db = utils.database.DBHandler()


@api.route("/sample1")
class Sample1Resource(Resource):
    @api.marshal_with(ManagementDto.SampleResponse)
    def get(self):
        """ get sample1 """
        return "sample"


@api.route("/sample2/<input>")
class Sample2Resource(Resource):
    @api.marshal_with(ManagementDto.SampleResponse, envelope="result")
    @api.doc(params={'input' : 'sample input'})
    def get(self, input):
        """ get sample2 """
        _flag, records = db.executer(query='''SELECT * FROM users;''')
        return records
