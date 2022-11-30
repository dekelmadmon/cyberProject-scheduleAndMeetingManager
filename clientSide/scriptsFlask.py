from flask import Flask, render_template, request
app = Flask(__name__)


@app.route('/')
def home():
   return render_template('theWeb.html')


def main_page():
   return render_template('home.html')


@app.route('/api/saveactivity', methods=["POST"])
def postDB():
    print(request.json)
    return request.form['name']


if __name__ == '__main__':
   app.run(host="10.42.100.82", port=80, debug=True)

