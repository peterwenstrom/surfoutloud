from flask import Flask
from flask_mysqldb import MySQL

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

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_HOST'] = 'sql11.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql11166771'
app.config['MYSQL_PASSWORD'] = 'vlgFFX7C1v'
app.config['MYSQL_DB'] = 'sql11166771'
mysql = MySQL(app)


@app.route('/api/dbtest')
def dbtest():
    cur = mysql.connection.cursor()
    cur.execute('''SELECT * FROM Person''')
    rv = cur.fetchall()
    return str(rv[1])


if __name__ == "__main__":
    app.run(debug=True)
