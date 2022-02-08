
from flask import Flask, jsonify, request
import utils.database

app = Flask(__name__)

db_handler = utils.database.DBHandler()

@app.route('/', methods=['GET'])
def vist():
    if request.method == "GET":
        data = db_handler.session('''SELECT * FROM users;''')
        # db_handler.Open()
        # data = db_handler.Execute('''SELECT * FROM users;''')
        print(data)
        return jsonify({"dd":"dd"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5040', debug=True)