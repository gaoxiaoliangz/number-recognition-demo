"""server"""
from flask import Flask, url_for, render_template
app = Flask(__name__)

strg = "thinking about "

# @app.route("/<string:name>")
# def move(name):
#   return strg + name

@app.route('/')
def index():
  return render_template('index.html', title='recog number')


if __name__ == '__main__':
  # url_for('static', filename='style.css')
  app.run()
