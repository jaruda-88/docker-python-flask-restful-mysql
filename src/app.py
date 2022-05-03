from flask import Flask

from utils.settings import BuildType


def register_blueprints(app):
    from src import blueprint
    from src.users.user_search import bp as UserSearch
    from src.boards.board_rd import bp as BoardRD
    from src.comments.comment_rd import bp as CommentRd

    app.register_blueprint(blueprint, url_prefix="/api")
    app.register_blueprint(UserSearch)
    app.register_blueprint(BoardRD)
    app.register_blueprint(CommentRd)


def create_swagger(app):
    from flasgger import Swagger
    from utils.settings import SWAGGER_CONFIG, SWAGGER_TEMPLATE

    Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)


def init_db():
    import os
    from pathlib import Path
    import databases as db
    from utils.settings import DATABASE_CONFIG as con
    import sys

    dbh = db.DBHandler(host=con['host'], port=con['port'], database=con['db_name'], user=con['user'], pw=con['pw'])

    try:
        root = Path(os.path.dirname(os.path.abspath(__file__))).parent
        path = os.path.join(root, 'utils/init_db.sql')

        data = open(path, 'r').readlines()

        dbh.executer_file_list(file_list=data)
    except Exception as ex:
        print(ex.args[0],file=sys.stderr)


def create_app():
    from flask_cors import CORS
    from utils.settings import BUILD_TYPE        

    app = Flask(__name__)

    CORS(app)

    if BUILD_TYPE != BuildType.SERVER:
        init_db()

    register_blueprints(app)    

    create_swagger(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='5040', debug=True)