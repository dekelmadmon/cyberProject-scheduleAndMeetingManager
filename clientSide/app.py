import json
import datetime
from flask import Flask, render_template, request, make_response
from src import sqliteDBModule as DBM
from src import client

class MeetingSchedulerApp:
    def __init__(self):
        self.app = Flask(__name__)

        self.app.route('/main')(self.main_page)
        self.app.route('/')(self.home_page)
        self.app.route('/login-page')(self.login_page)
        self.app.route('/sign-in-page')(self.sign_in_page)
        self.app.route('/api/save-activity', methods=["POST"])(self.post_new_activity)
        self.app.route('/api/login', methods=["POST"])(self.login_info)
        self.app.route('/api/sign-in', methods=["POST"])(self.sign_in_info)
        self.app.route('/update_schedule_dates', methods=["POST"])(self.update_dates)
        self.app.route('/request-meeting', methods=['POST'])(self.request_meeting)

    def start(self):
        self.app.run(host="127.0.0.1", port=80, debug=True)

    def main_page(self):
        return render_template('main.html')

    def home_page(self):
        return render_template('home.html')

    def login_page(self):
        return render_template("login.html")

    def sign_in_page(self):
        return render_template("sign_in.html")

    def post_new_activity(self):
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        return json_data, 200

    def login_info(self):
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        print(json_data)
        email = json_data['email']
        password = json_data['password']
        db = DBM.Database()
        if db.login_able(email, password):
            return 'approved', 200
        else:
            return "Invalid credentials", 401

    def sign_in_info(self):
        data = request.data.decode('utf-8')
        json_data = json.loads(data)
        username = json_data["username"]
        email = json_data['email']
        password = json_data['password']
        db = DBM.Database()
        if db.sign_in(username, email, password):
            return '', 200
        else:
            return 'Invalid credentials or user exists', 401

    def update_dates(self):
        try:
            data = request.data.decode('utf-8')
            json_data = json.loads(data)
            last_sunday = self.last_sunday_date()
            response_data = str(last_sunday + datetime.timedelta(json_data['factor'] - 1))
            this_date = json.dumps({"data": response_data})
            return make_response(this_date, 200)
        except json.JSONDecodeError:
            return make_response(json.dumps({"error": "Invalid JSON data"}), 400)
        except KeyError:
            return make_response(json.dumps({"error": "Missing key in JSON data"}), 400)

    def last_sunday_date(self):
        today = datetime.date.today()
        days_since_sunday = today.weekday() + 1
        last_sunday = today - datetime.timedelta(days=days_since_sunday)
        return last_sunday

    def request_meeting(self):
        attendee = request.json['attendee']
        sender = request.json['sender']
        date = request.json['date']
        message = {'type': 'request-meeting', 'attendee': attendee}
        client.request_meeting(attendee, sender, date)
        # return a response to the client
        return {'status': 'ok'}


if __name__ == '__main__':
    app = MeetingSchedulerApp()
    app.start()
