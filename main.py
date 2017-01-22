"""server"""
import base64
import io
import os

import numpy
from flask import Flask, jsonify, render_template, request, url_for

from PIL import Image, ImageFilter

app = Flask(__name__)

# strg = "thinking about "
# @app.route("/<string:name>")
# def move(name):
#   return strg + name

@app.route('/')
def index():
  return render_template('index.html', title='recog number')

@app.route('/upload', methods=['POST'])
def upload_img():
  # 1
  img_str = request.form['img'][22:]
  img_data = base64.b64decode(img_str)
  print(type(img_data))
  # print(img_data.read())
  img_obj = Image.open(io.BytesIO(img_data))
  # print(type(img_obj))

  img_pix = img_obj.load()
  print(img_obj.size)
  print(img_pix[0, 1])
  print(type(img_pix))

  # 2
  # img_data = Image.open('pic2.png')
  # print(img_data.size)

  # 3 ok
  # img_data = open('dw.jpg', 'rb')
  # # print(img_data.read())
  # # print(img_data.seek())
  # # print(img_data.tell())
  # img_obj = Image.open(img_data)
  # img_pix = img_obj.load()
  # print(img_obj.size)
  # print(img_pix[0, 1])  

  #Display image
  # im.show()
  # im_sharp = im.filter( ImageFilter.SHARPEN )
  # r,g,b = im_sharp.split()
  # print(r)


  # write image
  # leniyimg = open('imgout.png','wb')
  # leniyimg.write(imgData)
  # leniyimg.close()

  return jsonify(ok=1)

if __name__ == '__main__':
  app.run()
