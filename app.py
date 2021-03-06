from flask import jsonify
from flask import Flask, request
import db_handler

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/get_user', methods=['POST'])
def login():
    user_data = None
    request_data = request.get_json()
    print(request_data, file=open("values.log", 'w+'))
    if request.method == 'POST':
        user_data = {
            "photo": request_data['photo'],
            "first_name": request_data['firstname'],
            "last_name": request_data['lastname'],
            "email": request_data['email'],
            "gender": request_data['gender'],
            "pref": request_data['pref']
        }
    uid = db_handler.get_user(user_data)
    return jsonify({"id":uid})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
