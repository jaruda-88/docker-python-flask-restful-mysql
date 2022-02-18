from flask_restx import Resource
from .dto import ManagementDto

api = ManagementDto.api


@api.route("/")
class TestResource(Resource):
    @api.marshal_with(ManagementDto.test)
    def get(self):
        """ get test """
        return "test"
