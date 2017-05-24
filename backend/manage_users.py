from config import app, mysql, bcrypt
from flask import jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({'message': 'Username and password cannot be empty'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT password FROM User where username = %s''', [username])
    row = cursor.fetchall()
    # check credentials against DB
    if not row or not bcrypt.check_password_hash(row[0][0], password):
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
        cursor.execute('''INSERT INTO User VALUES (0, %s, %s)''', (username, password_hash))
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
def authorize():
    username = request.json.get('username', None)
    if get_jwt_identity() == username:
        response = {'message': 'Authorized user'}
        return jsonify(response), 200
    else:
        response = {'message': 'Username and token does not match'}
        return jsonify(response), 401


@app.route('/editusername', methods=['POST'])
@jwt_required
def edit_username():
    new_username = request.json.get('username', None)
    if not new_username:
        return jsonify({'message': 'New username cannot be empty'}), 400

    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT * FROM User where username = %s''', [new_username])
    row = cursor.fetchall()
    if row:
        return jsonify({'message': 'Username already exists'}), 409
    cursor.execute('''UPDATE User set username = %s where username = %s''', (new_username, get_jwt_identity()))
    mysql.connection.commit()

    response = {'access_token': create_access_token(identity=new_username),
                'username': new_username}
    return jsonify(response), 200
