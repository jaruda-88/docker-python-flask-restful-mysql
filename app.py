from flask import Flask


def register_blueprints(app):
    from src import blueprint

    app.register_blueprint(blueprint, url_prefix="/api")


def create_swagger(app):
    from flasgger import Swagger
    from utils.settings import SWAGGER_CONFIG, SWAGGER_TEMPLATE

    Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)


def create_app():
    app = Flask(__name__)

    register_blueprints(app)    

    create_swagger(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='5040', debug=True)