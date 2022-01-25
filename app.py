
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

app.secret_key = 'project1'

app.config['MYSQL_HOST'] = '13.124.47.173'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'project1'
app.config['MYSQL_PORT'] = 3306

# Intialize MySQL
mysql = MySQL(app)


@app.route('/', methods=['GET'])
def vist():
    if request.method == "GET":
        cur = mysql.connection.cursor()
        sql = "SELECT *FROM users"
        cur.execute(sql)
        
        data = cur.fetchall()
        cur.close()
        print(data)
        return jsonify({"dd":"dd"})

if __name__ == '__main__':
    app.run(debug=True)