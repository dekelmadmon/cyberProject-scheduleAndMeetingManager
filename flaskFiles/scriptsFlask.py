from flask import Flask, render_template
app = Flask(__name__)


@app.route('/')
def home():
   return render_template('theWeb.html')


def main_page():
   return render_template('home.html')


if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)

