from flask import Flask, render_template, request, jsonify
import json
import sys
sys.path.append(r'C:\Users\dekel\PycharmProjects\cyberProject-scheduleAndMeetingManager\src')
print(sys.path)
from src import sqliteDBModules as DBM
app = Flask(__name__)

DB = DBM.Database()
@app.route('/main')
def main_page():
   return render_template('theWeb.html')

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/sign-in')
def sign_in_page():
    return render_template("sign-in.html")

@app.route('/api/save-activity', methods=["POST"])
def post_new_activity():
    data = request.data.decode('utf-8')
    json_data = json.loads(data)
    print(json_data['name'])
    return json_data

@app.route('/api/sign-in-info', methods=["post"])
def sign_in_info():
    data = request.data.decode('utf-8')
    json_data = json.loads(data)
    print(json_data['username'])
    print(json_data['password'])
    return render_template('theWeb.html')


if __name__ == '__main__':
   app.run(host="127.0.0.1", port=80, debug=True)

