
from flask import Flask, jsonify, request
import sql

app = Flask(__name__)

db_handler = sql.DBHandler()

@app.route('/', methods=['GET'])
def vist():
    if request.method == "GET":
        db_handler.Open()
        data = db_handler.Execute('''SELECT * FROM users;''')
        print(data)
        db_handler.Close()
        return jsonify({"dd":"dd"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5040', debug=True)