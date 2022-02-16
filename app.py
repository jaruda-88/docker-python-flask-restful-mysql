
from flask import Flask, jsonify, request
import utils.database

app = Flask(__name__)

db_handler = utils.database.DBHandler()

@app.route('/', methods=['GET'])
def vist():
    if request.method == "GET":
        data = db_handler.select('''SELECT * FROM users;''')
        return jsonify({"dd":data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5040', debug=True)