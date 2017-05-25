from config import app, mysql
from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity


def validate_members(members):

    cursor = mysql.connection.cursor()
    member_ids = []
    for member in members:
        cursor.execute('''SELECT id FROM User where username = %s''', [member])
        row = cursor.fetchall()
        if row:
            member_ids.append(row[0])
    return member_ids


def add_members(members_ids, project_id):
    cursor = mysql.connection.cursor()

    for member_id in members_ids:
        try:
            cursor.execute('''INSERT INTO Member VALUES (0, %s, %s)''', (project_id, member_id))
            mysql.connection.commit()
        except:
            mysql.connection.rollback()
            response = {'msg': 'Something went wrong, please try again.'}
            return jsonify(response), 400
        return "herueka!"


@app.route('/getmembers', methods=['POST'])
def get_members():
    project_id = request.json.get('project_id', None)
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT memberid FROM Member where projectid = %s''', [project_id])
    rows = cursor.fetchall()
    members = []
    for row in rows:
        cursor.execute('''SELECT username FROM User where id = %s''', [row])
        members.append(cursor.fetchall()[0])

    return jsonify({'members': members}), 200


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


@jwt_required
@app.route('/addproject', methods=['POST'])
def add_project():
    admin = request.json.get('admin', None)
    members = request.json.get('new_members', None)
    project_name = request.json.get('name', None)
    project_description = request.json.get('description', None)
    if not project_description or not project_name:
        return jsonify({'message': 'Please enter a project name and description'}), 400
    if members:
        members.append(admin)
        members = list(set(members))
        members_ids = validate_members(members)

    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''INSERT INTO Project VALUES (0, %s, %s, %s)''',
                       (admin, project_name, project_description))
        cursor.execute('''SELECT max(id) FROM Project''')
        row = cursor.fetchall()
        project_id = row[0]
        mysql.connection.commit()

        add_members(members_ids, project_id)

        response = {'username': admin, 'project_id': row[0]}
        return jsonify(response)
    except:
        mysql.connection.rollback()
        response = {'msg': 'Something went wrong, please try again.'}
        return jsonify(response), 400
