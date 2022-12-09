from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)


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

@app.route('/api/new-user-info', methods=["post"])
def login_info():

    return render_template('theWeb.html')


if __name__ == '__main__':
   app.run(host="127.0.0.1", port=80, debug=True)

