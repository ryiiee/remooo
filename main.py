from flask import Flask, make_response, jsonify, Response, request
from flaskext.mysql import MySQL
from flask_mysqldb import MySQL
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

USER_DATA = {"Login": "Login"}

@auth.verify_password
def verify(username, password):
    if not (username and password):
        return False
    return USER_DATA.get(username) == password


app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_PASSWORD'] = 'apzx0dfd6'
app.config['MYSQL_DB'] = 'badmiton_reservation'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/')
def hello_world():
    return "<p>This is my list!</p>"

def data_fetch(query):
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()
    return data

@app.route("/friends", methods=["GET"])
@auth.login_required
def get_friends():
    data = data_fetch("""SELECT * FROM friends""")
    return make_response(jsonify(data), 200)


@app.route("/friends/<int:id>", methods=["GET"])
@auth.login_required
def get_friends_by_id(id):
    data = data_fetch("""SELECT * FROM freind WHERE friends_id = {}""".format(id))
    myResponse = make_response(jsonify(data))
    return myResponse
    

@app.route("/friends", methods=['POST'])
@auth.login_required
def add_friends():
    cur = mysql.connection.cursor()
    json = request.get_json(force=True)
    friends_name = json["friends_name"]
    friends_email = json["friends_email"]
    friends_contact = json["friends_contact"]
    cur.execute(
        """ INSERT INTO friends (friends_name, friends_email, friends_contact) VALUE (%s, %s, %s)""", (friends_name, friends_email, friends_contact),
    )
    mysql.connection.commit()
    _response = jsonify("friends added successfully!")
    _response.status_code = 200
    cur.close()
    return _response

@app.route("/friends/<int:id>", methods=["PUT"])
@auth.login_required
def update_friends_by_id(id):
    cur = mysql.connection.cursor()
    json = request.get_json(force=True)
    friends_name = json["friends_name"]
    friends_email = json["friends_email"]
    friends_contact = json["friends_contact"]
    cur.execute(""" UPDATE friends SET friends_name = %s, friends_email = %s, friends_contact = %s WHERE friends_id = %s""", (friends_name, friends_email, friends_contact, id))
    mysql.connection.commit()
    _response = jsonify("friends updated successfully!")
    _response.status_code = 200
    cur.close()
    return _response
        
        
        

@app.route("/friends/<int:id>", methods=["DELETE"])
@auth.login_required
def delete_friends(id):
    cur = mysql.connection.cursor()
    cur.execute(""" DELETE FROM friends WHERE friends_id = %s""", (id,))
    mysql.connection.commit()
    cur.close()
    return make_response(jsonify({"message": "friends deleted successfully"}), 200)
    


@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

if __name__ == "__main__":
    app.run(debug=True)