from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, send
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_bcrypt import Bcrypt


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
mysql = MySQL(app)

app.config['SECRET_KEY'] = 'asupersecretsecret'

socketio = SocketIO(app)
CORS(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({'message': 'Username and password cannot be empty'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT password FROM User where username = %s''', [username])
    row = cursor.fetchall()
    db_password = row[0][0]
    # check credentials against DB
    if not row or not bcrypt.check_password_hash(db_password, password):
        return jsonify({'message': 'Wrong username or password'}), 401

    response = {'access_token': create_access_token(identity=username),
                'username': username}
    return jsonify(response), 200


@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    repeat_password = request.json.get('repeat_password', None)
    if not username or not password or not repeat_password:
        return jsonify({'message': 'Username and password cannot be empty'}), 400
    elif password != repeat_password:
        return jsonify({'message': 'The passwords are not identical, please try again'}), 400

    # check DB
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM User where username = %s''', [username])
    row = cursor.fetchall()
    if row:
        return jsonify({'message': 'Username already exists'}), 409

    password_hash = bcrypt.generate_password_hash(password)

    # create new user in DB

    try:
        cursor.execute('''INSERT INTO User VALUES (0, %s, %s)''', (username.title(), password_hash))
        mysql.connection.commit()
        response = {'access_token': create_access_token(identity=username),
                    'username': username}
        return jsonify(response), 200
    except:
        mysql.connection.rollback()
        response = {'message': 'Something went wrong, please try again.'}
        return jsonify(response), 400


@app.route('/auth', methods=['POST'])
@jwt_required
def authorise():
    username = request.json.get('username', None)
    if get_jwt_identity() == username:
        response = {'message': 'Authorised user'}
        return jsonify(response), 200
    else:
        response = {'message': 'Username and token does not match'}
        return jsonify(response), 401

@app.route('/test_token')
@jwt_required
def test_token():
    return get_jwt_identity()

#Todo: need to fix so duplicate memberID:s can be assigned to duplicate projectID:s?
def addMember(members, projectId):
    cursor = mysql.connection.cursor()
    for x in members:
        cursor.execute('''SELECT id FROM User where username = %s''', [x])
        row = cursor.fetchall()
        testid = row[0]
        if row:
            try:
                cursor.execute('''INSERT INTO Member VALUES (0, %s, %s)''', (projectId,testid))
                mysql.connection.commit()
                #Todo: make an array of usernames that can be sent back to client
                #response = {'username': username, 'msg': 'everything went well, ' + username + ' is added'}
            except:
                mysql.connection.rollback()
                response = {'msg': 'Something went wrong, please try again.'}
                return jsonify(response), 400
    return "herueka!"



@app.route('/addproject', methods=['POST'])
def addProject():
    admin = request.json.get('username', None)
    members = request.json.get('memberArray', None)
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT username FROM User where username = %s''', [admin])
    row = cursor.fetchall()
    if row:
        try:
            cursor.execute('''INSERT INTO Project VALUES (0, %s)''', [admin])
            cursor.execute('''SELECT max(id) FROM Project''')
            row = cursor.fetchall()
            projectId = row[0]
            mysql.connection.commit()
            response = {'username': admin, 'projectid': row[0]}
            addMember(members,projectId)
            return jsonify(response)
        except:
            mysql.connection.rollback()
            response = {'msg': 'Something went wrong, please try again.'}
            return jsonify(response), 400


    # Only saved as a reference. Table Person is dropped...
    # @app.route('/')
    # def db_test():
    #     cur = mysql.connection.cursor()
    #     cur.execute('''SELECT * FROM Person''')
    #     rv = cur.fetchall()
    #     return str(rv[1])


@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

if __name__ == "__main__":
    socketio.run(app)
    # app.run(debug=True)