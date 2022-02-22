from flask import Flask
from flasgger import Swagger
from settings import SWAGGER_CONFIG, SWAGGER_TEMPLATE


def register_blueprints(app):
    from src import blueprint

    app.register_blueprint(blueprint, url_prefix="/api")


def create_app():
    app = Flask(__name__)

    register_blueprints(app)    

    Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)

    return app


if __name__ == '__main__':
    app = create_app()

    app.run(host='0.0.0.0', port='5040', debug=True)

#import utils.database
#db_handler = utils.database.DBHandler()

# @app.route('/', methods=['GET'])
# def vist():
#     if request.method == "GET":
#         _flag, data = db_handler.executer('''SELECT * FROM users;''')
#         return jsonify({"dd":data})