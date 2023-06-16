import datetime
import json
import sqlite3
import threading

from click import confirm
from flask import has_request_context
from flask import Flask, render_template, jsonify, request
from src import sqliteDBModule as DBM
from src import client_pupet
import logging
from sys import argv
from threading import Thread
from jinja2 import Template



class MeetingSchedulerApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.setup_logging()
        self.db = DBM.Database()
        self.client = None
        self.email = None
        self.app.config['SERVER_NAME'] = '127.0.0.1:' + argv[1]
        self.app.config['APPLICATION_ROOT'] = '/'  # Replace with your desired application root
        self.app.config['PREFERRED_URL_SCHEME'] = 'http'  # Replace with your preferred URL scheme (http or https)
        @self.app.after_request
        def after_request_handler(response):
            return self.check_email_cookie(response)

    # Rest of the code...

    def start(self):
        try:
            flask_thread = threading.Thread(target=self.app.run, kwargs={'host': '127.0.0.1', 'port': int(argv[1])})
            flask_thread.start()

            self.socket_client()
        except sqlite3.DatabaseError:
            self.logger.error('Error while connecting to SQLite database. Resetting the database...')
            self.db.reset_database()
            self.logger.info('Database reset successful. Starting the application...')
            self.start()

    def check_email_cookie(self, response):
        if has_request_context():
            cookie_header = request.headers.get('Cookie')
            if cookie_header is not None:
                cookie_parts = cookie_header.split('email=')
                if len(cookie_parts) > 1:
                    email = cookie_parts[1].split(';')[0]
                    self.socket_client()
        return response



    def setup_routes(self):
        self.app.route('/main')(self.main_page)
        self.app.route('/')(self.home_page)
        self.app.route('/login-page')(self.login_page)
        self.app.route('/sign-in-page')(self.sign_in_page)
        self.app.route('/api/save-activity', methods=["POST"])(self.post_new_activity)
        self.app.route('/api/login', methods=["POST"])(self.login_info)
        self.app.route('/api/sign-in', methods=["POST"])(self.sign_in_info)
        self.app.route('/update_schedule_dates', methods=["POST"])(self.update_dates)
        self.app.route('/request-meeting', methods=['POST'])(self.request_meeting)
        self.app.route('/recieve-meetings', methods=['GET'])(self.recieve_meetings)
        self.app.route('/get_email_cookie', methods=['GET'])(self.get_email_cookie)
        self.app.route('/notify-meeting-request/<sender>/<date>')(self.render_notify_meeting_request)

        # ...

    def render_notify_meeting_request(self, sender, date):
        return self.notify_meeting_request(sender, date)
    def socket_client(self):
        with self.app.app_context():
            self.email = self.get_email_cookie()
            if self.email is not None and self.client is None:  # Check if client already exists
                self.client = client_pupet.SocketClient('localhost', 18080, self.email)
                client_thread = threading.Thread(target=self.client.start)
                client_thread.daemon = True
                client_thread.start()
                return 'Client created'
            return 'Client already exists or email was None'

    def get_email_cookie(self):
        email = request.headers.get('Cookie').split('email=')[1].split(';')[0]
        return email

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def render_template(template_name):
        return render_template(template_name)
    @staticmethod
    def render_meeting_request(sender,date):
        return render_template('meeting_request.html', sender=sender, date=date)
    def home_page(self):
        return self.render_template('home.html')

    def login_page(self):
        return self.render_template('login.html')

    def sign_in_page(self):
        return self.render_template('sign_in.html')

    def main_page(self):
        return self.render_template('main.html')

    @staticmethod
    def get_json_data():
        return request.get_json()

    def post_new_activity(self):
        json_data = self.get_json_data()
        response = jsonify(response='Received new activity: {}'.format(json_data))
        self.logger.info('Post new activity response: %s', response.json)
        return response, 200

    def login_info(self):
        json_data = self.get_json_data()
        self.email = json_data.get('email')
        password = json_data.get('password')
        db = DBM.Database()
        if db.authenticate_user_credentials(self.email, password):
            response = jsonify(response='Login successful')
            self.logger.info('Login response: %s', response.json)
            return response, 200
        else:
            response = jsonify(response='Invalid credentials')
            self.logger.info('Login response: %s', response.json)
            return response, 401

    def sign_in_info(self):
        json_data = self.get_json_data()
        username = json_data.get('username')
        self.email = json_data.get('email')
        password = json_data.get('password')
        db = DBM.Database()
        if db.sign_in(username, self.email, password):
            response = jsonify(response='Sign-in successful')
            self.logger.info('Sign-in response: %s', response.json)
            return response, 200
        else:
            response = jsonify(response='Invalid credentials or user exists')
            self.logger.info('Sign-in response: %s', response.json)
            return response, 401

    def update_dates(self):
        json_data = self.get_json_data()
        factor = json_data.get('factor')
        if factor is None:
            response = jsonify(error='Missing "factor" in JSON data')
            self.logger.info('Update dates response: %s', response.json)
            return response, 400

        last_sunday = self.last_sunday_date()
        response_data = str(last_sunday + datetime.timedelta(days=factor - 1))
        response = jsonify(response='Updated dates: {}'.format(response_data))
        self.logger.info('Update dates response: %s', response.json)
        return response, 200

    @staticmethod
    def last_sunday_date():
        today = datetime.date.today()
        days_since_sunday = today.weekday() + 1
        last_sunday = today - datetime.timedelta(days=days_since_sunday)
        return last_sunday

    def request_meeting(self):
        attendee = request.json.get("attendee")
        date = request.json.get("date")
        if attendee and date:
            self.client.send_create_invitation(date, attendee)  # Pass the date to the send_create_invitation method
            response = jsonify(response='Meeting requested successfully')
            self.logger.info('Request meeting response: %s', response.json)
            return response, 200
        self.logger.info('Request meeting response: declined insufficient data')
        return '', 400

    def recieve_meetings(self):
        response = self.client.send_receive_invitation()
        #response = jsonify(response='Check successfully')
        self.logger.info('Check meetings response: %s', response.json)
        return response, 200


    def get_activities_by_date(self):
        date = request.args.get('date')
        useremail = request.args.get('useremail')
        db = DBM.Database()
        activities = db.get_activities_by_date(date, useremail)
        return jsonify(activities)

    def notify_meeting_request(self, sender, date):
        with self.app.app_context():
            rendered_template = self.render_meeting_request(sender, date)
            return rendered_template

def main():
    app = MeetingSchedulerApp()
    app.start()

if __name__ == '__main__':
    main()
