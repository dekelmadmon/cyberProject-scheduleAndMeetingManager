import json
import datetime
from flask import Flask, render_template, request, make_response
from src import sqliteDBModule as DBM

app = Flask(__name__)

DB = DBM.Database()


@app.route('/main')
def main_page():
    return render_template('main.html')


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route('/login-page')
def login_page():
    return render_template("login.html")


@app.route('/sign-in-page')
def sign_in_page():
    return render_template("sign_in.html")


@app.route('/api/save-activity', methods=["POST"])
def post_new_activity():
    data = request.data.decode('utf-8')
    json_data = json.loads(data)
    return json_data


@app.route('/api/sign-in', methods=["post"])
def sign_in_info():
    data = request.data.decode('utf-8')
    json_data = json.loads(data)
    print(json_data)
    username = json_data["username"]
    email = json_data['email']
    password = json_data['password']
    if DB.sign_in(username, email, password):
        return '', 200
    else:
        return "Invalid credentials", 401


@app.route('/api/login', methods=["POST"])
def login_info():
    data = request.data.decode('utf-8')
    json_data = json.loads(data)
    print(json_data)
    email = json_data['email']
    password = json_data['password']

    if DB.login(email, password):
        return '', 200
    else:
        return "Invalid credentials", 401


@app.route('/update_schedule_dates', methods=["post"])
def update_dates():
    """
    the function gets the number of clicks you did on the week button in the array of dates in json
    :return: returns an objects of dates to the client to update the dates on the array in html
    """
    try:
        data = request.data.decode('utf-8')
        print("data-", data)
        json_data = json.loads(data)
        print("json data ", json_data["factor"])

        last_sunday = last_sunday_date()
        print(last_sunday)
        response_data = (str(last_sunday + datetime.timedelta(json_data['factor'] - 1)))
        this_date = json.dumps({"data": response_data})

        print("this_date = ", this_date)

        return make_response(this_date)
    except json.JSONDecodeError as e:
        # handle JSON decoding errors, e.g. return a 400 Bad Request response
        return make_response(json.dumps({"error": "Invalid JSON data"}), 400)
    except KeyError as e:
        # handle missing key errors, e.g. return a 400 Bad Request response
        return make_response(json.dumps({"error": "Missing key in JSON data"}), 400)


def last_sunday_date():
    today = datetime.date.today()
    print(today)
    days_since_sunday = 6 - today.weekday()
    print(days_since_sunday)
    last_sunday = today - datetime.timedelta(days=days_since_sunday)
    return last_sunday


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=80, debug=True)
