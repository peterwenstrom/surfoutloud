from config import app, mysql
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


# Todo: need to fix so duplicate memberID:s can be assigned to duplicate projectID:s?
def add_member(members, project_id):
    cursor = mysql.connection.cursor()
    for x in members:
        cursor.execute('''SELECT id FROM User where username = %s''', [x])
        row = cursor.fetchall()
        test_id = row[0]
        if row:
            try:
                # projectId, MemberId
                cursor.execute('''INSERT INTO Member VALUES (0, %s, %s)''', (project_id, test_id))
                mysql.connection.commit()
                # Todo: make an array of usernames that can be sent back to client
                # response = {'username': username, 'msg': 'everything went well, ' + username + ' is added'}
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
def add_project():
    admin = request.json.get('username', None)
    members = request.json.get('memberArray', None)
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT id, username FROM User where username = %s''', [admin])
    row = cursor.fetchall()
    if row:
        try:
            cursor.execute('''INSERT INTO Project VALUES (0, %s)''', [admin])
            cursor.execute('''SELECT max(id) FROM Project''')
            row = cursor.fetchall()
            project_id = row[0]
            mysql.connection.commit()
            members.append(admin)
            response = {'username': admin, 'projectid': row[0]}
            add_member(members, project_id)
            return jsonify(response)
        except:
            mysql.connection.rollback()
            response = {'msg': 'Something went wrong, please try again.'}
            return jsonify(response), 400
