from flask import Flask, render_template
from src import utils
app=Flask(__name__)
@app.route('/')
def home():
   return render_template('theWeb.html')


if __name__ == '__main__':
   app.run(host="localhost", port=8080, debug=True)
