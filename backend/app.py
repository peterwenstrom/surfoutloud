from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, send
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity


class CustomFlask(Flask):
    jinja_options = Flask.jinja_options.copy()
    jinja_options.update(dict(
    block_start_string='$$',
    block_end_string='$$',
    variable_start_string='$',
    variable_end_string='$',
    comment_start_string='$#',
    comment_end_string='#$',
    ))


app = CustomFlask(__name__)
CORS(app)

# mysql = MySQL()

# MySQL configurations
app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql11166771'
app.config['MYSQL_PASSWORD'] = 'vlgFFX7C1v'
app.config['MYSQL_DB'] = 'sql11166771'
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'asupersecretsecret'
socketio = SocketIO(app)

jwt = JWTManager(app)


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    response = {'access_token': create_access_token(identity=username)}
    return jsonify(response), 200


@app.route('/')
@jwt_required
def dbtest():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM Person''')
    rv = cur.fetchall()
    return str(rv[1])
    # return get_jwt_identity()


@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app)
    # app.run(debug=True)