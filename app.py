from flask import Flask
from api import blueprint
from flasgger import Swagger


app = Flask(__name__)
app.register_blueprint(blueprint)

# SWAGGER SETTING
swagger_config = {
    "title": "SWAGGER TEST API",
    "uiversion": 3,
    "headers": [],
    "specs": [
        {
            "endpoint": 'swagger_test_api',
            "route": '/swagger_test_api_spec.json',
            "rule_filter": lambda rule:True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/help",
    "specs_route": "/help/"
}

swagger_template = {
    "swagger": "2.0",
    "info":{
        "title": "Swagger Test API",
        "description": "Api for test",
        "version": "1.0.0",
        "openapi_version": "3.0.2",
        "contact": {
            "name": "Test Channel",
            "url": "https://github.com/jaruda-88"
        }
    }
}

swagger = Swagger(app, config=swagger_config, template=swagger_template)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5040', debug=True)

#import utils.database
#db_handler = utils.database.DBHandler()

# @app.route('/', methods=['GET'])
# def vist():
#     if request.method == "GET":
#         _flag, data = db_handler.executer('''SELECT * FROM users;''')
#         return jsonify({"dd":data})