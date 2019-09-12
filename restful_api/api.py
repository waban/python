#!"C:\Python37\python.exe"
import cgi
from flask import Flask, jsonify
from flask_restful import Resource
from flaskext.mysql import MySQL

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = ''
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
mysql = MySQL(app)


mysql.init_app(app)

@app.route('/json/api/', methods=['GET'])
def index():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM //#table#// ')
    results = cursor.fetchall()
    payload = []
    content = {}
    for result in results:
        content = {
            'col1'   : result[0] ,
            'col2'   : result[1] ,
            'col3'   : result[2] ,
            'col4'   : result[3] ,
            'col5'   : result[4] ,
            'col6'   : result[5] ,
            'col7'   : result[6]            
        }
        payload.append(content)
        content = {}
    return jsonify(payload)

if __name__ == '__main__':
    app.run(debug=True)

