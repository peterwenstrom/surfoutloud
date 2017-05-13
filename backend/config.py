from flask import Flask
from flask_mysqldb import MySQL
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from datetime import timedelta


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

# MySQL configurations
app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql11166771'
app.config['MYSQL_PASSWORD'] = 'vlgFFX7C1v'
app.config['MYSQL_DB'] = 'sql11166771'

# JWT configurations
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SECRET_KEY'] = 'asupersecretsecret'

CORS(app)
JWTManager(app)
mysql = MySQL(app)
socketio = SocketIO(app)
bcrypt = Bcrypt(app)

