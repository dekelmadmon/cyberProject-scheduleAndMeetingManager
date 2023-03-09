import json

import datetime

from flask import Flask, render_template, request, make_response

from src import sqliteDBModule as DBM

app = Flask(__name__)

DB = DBM.Database()


@app.route('/main')
def main_page():
    return render_template('gpt_generated_html.html')


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


@app.route('/update_schedule_dates', methods=["post"])
def update_dates():
    """
    the function gets the number of clicks you did on the week button in the array of dates in json
    :return: returns an objects of dates to the client to update the dates on the array in html
    """
    data = request.data.decode('utf-8')
    json_data = json.loads(data)
    arr = []

    last_sunday = last_sunday_date()
    for i in range(7):
        arr.append(str(last_sunday + datetime.timedelta(json_data['factor'] + i - 1)))
        print(arr[i-1])
    return make_response(arr)


def last_sunday_date():
    today = datetime.date.today()
    days_since_sunday = today.weekday() + 1
    last_sunday = today - datetime.timedelta(days=days_since_sunday)
    return last_sunday


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=80, debug=True)
