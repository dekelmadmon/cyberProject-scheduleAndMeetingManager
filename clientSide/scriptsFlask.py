from flask import Flask, render_template, request, jsonify
import json
app = Flask(__name__)


@app.route('/')
def home():
   return render_template('theWeb.html')


def main_page():
   return render_template('home.html')


@app.route('/api/saveactivity', methods=["POST"])
def postDB():
    data = request.data.decode('utf-8')
    json_data = json.loads(data)
    print(json_data['name'])
    return json_data


if __name__ == '__main__':
   app.run(host="192.168.68.108", port=80, debug=True)

