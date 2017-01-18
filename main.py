"""server"""
from flask import Flask, url_for, render_template, request
app = Flask(__name__)

strg = "thinking about "

# @app.route("/<string:name>")
# def move(name):
#   return strg + name

@app.route('/')
def index():
  return render_template('index.html', title='recog number')

@app.route('/upload', methods=['POST'])
def upload_img():
  img=request.form['img']
  return img

if __name__ == '__main__':
  # url_for('static', filename='style.css')
  app.run()
