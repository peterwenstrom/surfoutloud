from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, send
from flask_cors import CORS
from flask_jwt import JWT, jwt_required, current_identity


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


class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


user = User(1, 'user', 'password')


def authenticate(username, password):
    if username == user.username and password == user.password:
        return user


def identity(payload):
    return user

app = CustomFlask(__name__)
CORS(app)

# mysql = MySQL()

# MySQL configurations
app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql11166771'
app.config['MYSQL_PASSWORD'] = 'vlgFFX7C1v'
app.config['MYSQL_DB'] = 'sql11166771'
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

jwt = JWT(app, authenticate, identity)


@app.route('/')
@jwt_required()
def dbtest():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM Person''')
    rv = cur.fetchall()
    return str(rv[1])


@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app)
    # app.run(debug=True)