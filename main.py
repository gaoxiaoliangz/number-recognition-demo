"""server"""
import base64
import io
import os

import numpy as np
import tensorflow as tf

from flask import Flask, jsonify, render_template, request, url_for
from tensorflow.examples.tutorials.mnist import input_data

from PIL import Image, ImageFilter

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


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


### tf start
## init

# placeholders
x = tf.placeholder(tf.float32, [None, 784])
y_ = tf.placeholder(tf.float32, [None, 10])

# variables
W = tf.Variable(tf.zeros([784, 10]), name='Weight') # weight
b = tf.Variable(tf.zeros([10])) # bias

# the model
y = tf.nn.softmax(tf.matmul(x, W) + b)

init = tf.global_variables_initializer()
sess = tf.Session()
sess.run(init)

def train():
  print('start training ...')
  cross_entropy = tf.reduce_mean(-tf.reduce_sum(
      y_ * tf.log(y), reduction_indices=[1]))

  train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

  for i in range(1000):
    batch_xs, batch_ys = mnist.train.next_batch(100)
    sess.run(train_step, feed_dict={x: batch_xs, y_: batch_ys})

  print('end training')
  # print(sess.run(W))


def test_image(raw_image):
  """test images"""

  print(sess.run(W))


  # # raw_image_32 = [float(raw_image_p) for raw_image_p in raw_image]
  # raw_image_32 = [np.float(raw_image_p) for raw_image_p in raw_image]
  # np_img = np.array(raw_image_32)
  # print(np.shape(np_img))
  # # print_image(np_img)
  # # print(np_img)
  # # print(len(np_img))
  # # print(type(np_img))
  

  # np_img = mnist.test.images[876]

  # # print(type(np_img[0]))

  # t_image = tf.pack([np_img], name='test_image')
  # result = tf.nn.softmax(tf.matmul(t_image, W) + b)
  # final_result = tf.argmax(result, 1)
  # py_res = sess.run(final_result)[0]

  # return py_res
  return 1

## tf end

app = Flask(__name__)
# print('wtf')
train()

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
  img_obj = Image.open(io.BytesIO(img_data))
  img_obj = img_obj.resize((28, 28))
  # print(type(img_obj))

  img_pix = img_obj.load()

  img_arr = []

  for index_b in range(28):
    for index_a in range(28):
      pix_l = img_pix[index_a, index_b][3]/255
      img_arr.append(pix_l)


  num = test_image(img_arr)
  num = 'wtf'
  



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

  return jsonify(ok=1, num=num)

if __name__ == '__main__':
  # train()
  app.run()
