import json
import sqlite3
import threading
import socket

from flask import has_request_context
from flask import render_template, jsonify, request
from flask import Flask, session

from src import client
import logging
from sys import argv


def get_ipv4():
    # Get the IPv4 address of the host
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address


class MeetingSchedulerApp:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.setup_logging()
        self.client = None
        self.app.secret_key = 'DekelIs%^#King'
        self.app.config['SERVER_NAME'] = get_ipv4() + ':' + argv[1]
        self.app.config['APPLICATION_ROOT'] = '/'  # Replace with your desired application root
        self.app.config['PREFERRED_URL_SCHEME'] = 'http'  # Replace with your preferred URL scheme (http or https)
        self.server_host = argv[2]
        self.server_port = int(argv[3])

        # Set up an after request handler to check the email cookie
        @self.app.after_request
        def after_request_handler(response):
            return self.check_email_cookie(response)

    def start(self):
        # Start the Flask application in a separate thread
        flask_thread = threading.Thread(target=self.app.run, kwargs={'host': get_ipv4(), 'port': int(argv[1])})
        flask_thread.start()

        # Start the socket client
        self.socket_client()

    def check_email_cookie(self, response):
        # Check if there is a request context and the 'email' cookie is present
        if has_request_context():
            cookie_header = request.headers.get('Cookie')
            if cookie_header is not None:
                cookie_parts = cookie_header.split('email=')
                if len(cookie_parts) > 1:
                    email = cookie_parts[1].split(';')[0]
                    self.socket_client()
        return response

    def setup_routes(self):
        # Define the routes for different pages and actions
        # Pages
        self.app.route('/main')(self.main_page)
        self.app.route('/')(self.home_page)
        self.app.route('/login-page')(self.login_page)
        self.app.route('/sign-in-page')(self.sign_in_page)

        # Actions
        self.app.route('/api/login', methods=["POST"])(self.login_info)
        self.app.route('/api/sign-in', methods=["POST"])(self.sign_in_info)
        self.app.route('/request-meeting', methods=['POST'])(self.request_meeting)
        self.app.route('/recieve-meetings', methods=['GET'])(self.recieve_meetings)
        self.app.route('/update-meeting', methods=['POST'])(self.update_meeting)
        self.app.route('/get_email_cookie', methods=['GET'])(self.get_email_cookie)

    def socket_client(self):
        with self.app.app_context():
            if self.client is None:  # Check if client already exists
                self.client = client.SocketClient(self.server_host, self.server_port)
                client_thread = threading.Thread(target=self.client.start)
                client_thread.daemon = True
                client_thread.start()
                return 'Client created'
            return 'Client already exists or email was None'

    def get_email_cookie(self):
        # Get the email from the 'email' cookie in the request headers
        if has_request_context() and request.headers.get('Cookie'):
            cookie_parts = request.headers.get('Cookie').split('email=')
            if len(cookie_parts) > 1:
                email = cookie_parts[1].split(';')[0]
                return email
        return None

    def setup_logging(self):
        # Set up basic logging configuration
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    @staticmethod
    def render_template(template_name):
        # Render a Jinja2 template
        return render_template(template_name)

    @staticmethod
    def render_meeting_request(sender, date):
        # Render the meeting request template with the sender and date
        return render_template('meeting_request.html', sender=sender, date=date)

    def checkUserInSession(self, user):
        # Check if the user is in the session (logged in)
        if 'username' in session:
            return session['username'] == user
        return False

    def home_page(self):
        # Render the home page template
        return self.render_template('home.html')

    def login_page(self):
        # Render the login page template
        return self.render_template('login.html')

    def sign_in_page(self):
        # Render the sign-in page template
        return self.render_template('sign_in.html')

    def main_page(self):
        # Render the main page template if the user is in session, otherwise redirect to the home page
        if self.checkUserInSession(self.get_email_cookie()):
            return self.render_template('main.html')
        return self.render_template('home.html')

    @staticmethod
    def get_json_data():
        # Get JSON data from the request
        return request.get_json()

    def login_info(self):
        # Handle login information request
        json_data = self.get_json_data()
        email = json_data.get('email')
        password = json_data.get('password')
        self.socket_client()
        if self.client.send_login_request(email, password):
            response = jsonify(response='Login successful')
            session['username'] = email
            self.logger.info('Login response: %s', response.json)
            return response, 200
        else:
            response = jsonify(response='Invalid credentials')
            self.logger.info('Login response: %s', response.json)
            return response, 401

    def sign_in_info(self):
        # Handle sign-in information request
        json_data = self.get_json_data()
        username = json_data.get('username')
        email = json_data.get('email')
        password = json_data.get('password')
        self.socket_client()
        if self.client.send_sign_in_request(username, email, password):
            response = jsonify(response='Sign-in successful')
            self.logger.info('Sign-in response: %s', response.json)
            return response, 200
        else:
            response = jsonify(response='Invalid credentials or user exists')
            self.logger.info('Sign-in response: %s', response.json)
            return response, 401

    def request_meeting(self):
        # Handle meeting request
        requester = self.get_email_cookie()
        attendee = request.json.get("attendee")
        date = request.json.get("date")
        if attendee and date:
            self.client.send_create_invitation(requester, date,
                                               attendee)  # Pass the date to the send_create_invitation method
            response = jsonify(response='Meeting requested successfully')
            self.logger.info('Request meeting response: %s', response.json)
            return response, 200
        self.logger.info('Request meeting response: declined insufficient data')
        return '', 400

    def update_meeting(self):
        # Handle meeting update request
        user = self.get_email_cookie()
        requester = request.json.get("requester")
        attendee = request.json.get("attendee")
        date = request.json.get("date")
        status = request.json.get("status")
        if attendee and date:
            self.client.send_update_invitation(user, requester, date, attendee,
                                               status)  # Pass the date to the send_create_invitation method
            response = jsonify(response='Meeting updated successfully')
            self.logger.info('Request update meeting response: %s', response.json)
            return response, 200
        self.logger.info('Request update meeting response: declined insufficient data')
        return '', 400

    def recieve_meetings(self):
        # Handle receive meetings request
        requester = self.get_email_cookie()
        response = self.client.send_receive_invitation(requester)

        # Ensure response is a JSON object
        if isinstance(response, str):
            response = json.loads(response)

        self.logger.info('Check meetings response: %s', response)
        return jsonify(response), 200


def main():
    app = MeetingSchedulerApp()
    app.start()


if __name__ == '__main__':
    main()
