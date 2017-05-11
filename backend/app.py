from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL
from flask_socketio import SocketIO, send, emit, join_room, leave_room, close_room, rooms, disconnect
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


@app.route('/getprojects', methods=['GET'])
@jwt_required
def get_projects():
    username = get_jwt_identity()
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT projectid FROM Member where memberid = (SELECT id FROM User where username = %s)''',
                   [username])
    rows = cursor.fetchall()
    projects = []
    for row in rows:
        cursor.execute('''SELECT * FROM Project where id = %s''', [row[0]])
        projects.append(cursor.fetchall()[0])

    return jsonify({'projects': projects}), 200


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


@socketio.on('sendInRoom')
def send_room_message(message):
    #session['receive_count'] = session.get('receive_count', 0) + 1
    emit('room_response',
         {'data': message['data'], 'room': message['room']},
         room=message['room'])

@socketio.on('join')
def join(message):
    join_room(message['room'])
    #session['receive_count'] = session.get('receive_count', 0) + 1
    emit('join_room_response',
         {'data': ",".join(rooms())})


if __name__ == "__main__":
    socketio.run(app)
    # app.run(debug=True)