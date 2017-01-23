"""server"""
import base64
import io
import os
import numpy as np
# import numpy
from flask import Flask, jsonify, render_template, request, url_for

from PIL import Image, ImageFilter

app = Flask(__name__)

# strg = "thinking about "
# @app.route("/<string:name>")
# def move(name):
#   return strg + name



def print_image(raw_image_data):
  """print image with '+' & '-'"""
  one_sample_image = np.array(raw_image_data).reshape([28, 28])
  for index_a in range(len(one_sample_image)):
    for index_b in range(len(one_sample_image[index_a])):
      if index_b == 27:
        print('')

      point = one_sample_image[index_a][index_b]

      if point > 0.3:
        print("+", end="")
      elif point > 0 and point <= 0.3:
        print("-", end="")
      else:
        print(" ", end="")




@app.route('/')
def index():
  return render_template('index.html', title='recog number')

@app.route('/upload', methods=['POST'])
def upload_img():
  # 1
  img_str = request.form['img'][22:]
  img_data = base64.b64decode(img_str)
  img_obj = Image.open(io.BytesIO(img_data))
  img_obj = img_obj.resize((28, 28))
  # print(type(img_obj))

  img_pix = img_obj.load()

  img_arr = []

  for index_b in range(28):
    for index_a in range(28):
      pix_l = img_pix[index_a, index_b][3]/255
      img_arr.append(pix_l)


  print_image(img_arr)




  # print(img_obj.size)
  # print(img_pix[0, 1])
  # print(type(img_pix))

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
