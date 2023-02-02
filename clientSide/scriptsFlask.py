from flask import Flask, render_template, request
import json
from src import sqliteDBModule as DBM
app = Flask(__name__)

DB = DBM.Database()


@app.route('/main')
def main_page():
    return render_template('main.html')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/login-page')
def login_page():
    return render_template("login.html")


@app.route('/sign-in-page')
def sign_in_page():
    return render_template("sign-in.html")


@app.route('/api/save-activity', methods=["POST"])
def post_new_activity():
    data = request.data.decode('utf-8')
    json_data = json.loads(data)

    return json_data


@app.route('/api/sign-in', methods=["post"])
def sign_in_info():
    data = request.data.decode('utf-8')
    json_data = json.loads(data)
    username = json_data['username']
    password = json_data['password']
    print(username + ", " + password)
    return render_template('main.html')


@app.route('/api/login', methods=["post"])
def login_info():
    data = request.data.decode('utf-8')
    json_data = json.loads(data)
    username = json_data['username']
    password = json_data['password']
    email = json_data['email']
    print(username + ", " + password + ", " + email)
    DB.user_exist(email)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=80, debug=True)
