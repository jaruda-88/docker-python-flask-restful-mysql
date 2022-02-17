from flask import Flask
from api import blueprint

app = Flask(__name__)
app.register_blueprint(blueprint)

#import utils.database
#db_handler = utils.database.DBHandler()

# @app.route('/', methods=['GET'])
# def vist():
#     if request.method == "GET":
#         _flag, data = db_handler.executer('''SELECT * FROM users;''')
#         return jsonify({"dd":data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5040', debug=True)