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
            member_ids.append(row[0][0])
    return member_ids


def add_members(members_ids, project_id):
    cursor = mysql.connection.cursor()

    for member_id in members_ids:
        try:
            cursor.execute('''INSERT INTO Member VALUES (0, %s, %s, 0)''', (project_id, member_id))
            mysql.connection.commit()
        except:
            mysql.connection.rollback()
            response = {'message': 'Something went wrong, please try again.'}
            return response
    return False


@app.route('/getmembers/<project_id>', methods=['GET'])
@jwt_required
def get_members(project_id):
    cursor = mysql.connection.cursor()
    cursor.execute('''SELECT memberid FROM Member where projectid = %s AND accepted = 1''', [project_id])
    rows = cursor.fetchall()
    members = []
    for row in rows:
        cursor.execute('''SELECT username FROM User where id = %s''', [row])
        members.append(cursor.fetchall()[0])

    return jsonify({'members': members}), 200


@app.route('/getprojects/<accepted>', methods=['GET'])
@jwt_required
def get_projects(accepted):
    username = get_jwt_identity()
    cursor = mysql.connection.cursor()
    cursor.execute(
        '''SELECT projectid FROM Member where memberid = (SELECT id FROM User where username = %s) AND accepted = %s''',
        (username, accepted))
    rows = cursor.fetchall()
    projects = []
    for row in rows:
        project = {}
        cursor.execute('''SELECT * FROM Project where id = %s''', [row[0]])
        project_row = cursor.fetchall()[0]
        # create neat project object instead of crazy db row
        project['id'] = project_row[0]
        project['admin'] = project_row[1]
        project['name'] = project_row[2]
        project['description'] = project_row[3]
        projects.append(project)

    return jsonify({'projects': projects}), 200


@app.route('/addproject', methods=['POST'])
@jwt_required
def add_project():
    admin = request.json.get('admin', None)
    members = request.json.get('new_members', None)
    project_name = request.json.get('name', None)
    project_description = request.json.get('description', None)
    if not project_description or not project_name:
        return jsonify({'message': 'Please enter a project name and description'}), 400

    cursor = mysql.connection.cursor()
    try:
        cursor.execute('''INSERT INTO Project VALUES (0, %s, %s, %s)''',
                       (admin, project_name, project_description))
        cursor.execute('''SELECT max(id) FROM Project''')
        project_id = cursor.fetchall()[0]

        mysql.connection.commit()

        cursor.execute('''SELECT id FROM User where username = %s''', [admin])
        admin_id = cursor.fetchall()[0]
        try:
            cursor.execute('''INSERT INTO Member VALUES (0, %s, %s, 1)''', (project_id, admin_id))
            mysql.connection.commit()
        except:
            mysql.connection.rollback()
            response = {'message': 'Something went wrong, please try again.'}
            return jsonify(response), 400

        members = list(set(members))
        members.remove(admin)
        members_ids = validate_members(members)
        error = add_members(members_ids, project_id)
        if error:
            return jsonify(error), 400
        response = {'admin': admin, 'id': project_id, 'description': project_description, 'name': project_name}
        return jsonify(response), 200
    except:
        mysql.connection.rollback()
        response = {'message': 'Something went wrong, please try again.'}
        return jsonify(response), 400
