"""server"""
from flask import Flask, url_for, render_template, request, jsonify
import os, base64

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
  img = request.form['img'][22:]

  # print(type(img))
  
  imgData = base64.b64decode(img)
  leniyimg = open('imgout.png','wb')
  leniyimg.write(imgData)
  leniyimg.close()

  # print(imgData)

  return jsonify(ok=1)

if __name__ == '__main__':
  # url_for('static', filename='style.css')
  app.run()
