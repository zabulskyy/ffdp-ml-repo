from flask import jsonify
from flask import Flask, request
import db_handler

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/summary')
def summary():
    d = {'result': 'Haha'}
    return jsonify(d)


@app.route('/get_user', methods=['POST'])
def login():
    user_data = None
    request.get_data()
    if request.method == 'POST':
        user_data = {
            "photo": request.form['photo'],
            "first_name": request.form['firstname'],
            "last_name": request.form['lastname'],
            "email": request.form['email'],
            "gender": request.form['gender'],
            "pref": request.form['pref']
        }
    uid = db_handler.get_user(user_data)
    return uid



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
