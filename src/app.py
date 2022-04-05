from flask import Flask


def register_blueprints(app):
    from src import blueprint

    app.register_blueprint(blueprint, url_prefix="/api")


def create_swagger(app):
    from flasgger import Swagger
    from utils.settings import SWAGGER_CONFIG, SWAGGER_TEMPLATE

    Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)


def init_db():
    import os
    from pathlib import Path
    import utils.database as database

    db = database.DBHandler()

    root = Path(os.path.dirname(os.path.abspath(__file__))).parent
    path = os.path.join(root, 'utils/init_db.sql')

    data = open(path, 'r').readlines()
    stmts = []
    DELIMITER = ';'
    stmt = ''

    for lineno, line in enumerate(data):
        if not line.strip():
            continue

        if line.startswith('--'):
            continue

        if 'DELIMITER' in line:
            DELIMITER = line.split()[1]
            continue

        if (DELIMITER not in line):
            stmt += line.replace(DELIMITER, ';')
            continue

        if stmt:
            stmt += line
            stmts.append(stmt.strip())
            stmt = ''
        else:
            stmts.append(line.strip())
     
    _flag, conn = db.connector()
    if _flag:
        with conn.cursor() as cursor:
            for stmt in stmts:
                cursor.execute(stmt)
            conn.commit()
            cursor.close()
        conn.close()


def create_app():
    from flask_cors import CORS
    from utils.settings import BUILD

    app = Flask(__name__)

    CORS(app)

    if BUILD['type'] != 'server':
        init_db()

    register_blueprints(app)    

    create_swagger(app)

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port='5040', debug=True)