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

def run_tf():
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


  def test_image(raw_image):
    raw_image_32 = [np.float(raw_image_p) for raw_image_p in raw_image]
    np_img = np.array(raw_image_32)
    t_image = tf.pack([np_img], name='test_image')
    result = tf.nn.softmax(tf.matmul(t_image, W) + b)
    final_result = tf.argmax(result, 1)
    py_res = sess.run(final_result)[0]

    return py_res


  def test_images():
    """test images"""
    raw_image_list = [
        mnist.test.images[image_index] for image_index in [22, 456, 876, 8765]
    ]

    print(np.shape(raw_image_list[0]))

    for raw_image in raw_image_list:
      print_image(raw_image)
      test_image = tf.pack([raw_image])
      result = tf.nn.softmax(tf.matmul(test_image, W) + b)
      final_result = tf.argmax(result, 1)

      print("number is: ", end="")
      print(sess.run(final_result)[0])
      print("---")

  train()
  test_images()
  ### tf end




app = Flask(__name__)


@app.route('/')
def index():
  return render_template('index.html', title='recog number')


@app.route('/upload', methods=['POST'])
def upload_img():
  img_str = request.form['img'][22:]
  img_data = base64.b64decode(img_str)
  img_obj = Image.open(io.BytesIO(img_data))
  img_obj = img_obj.resize((28, 28))
  img_pix = img_obj.load()
  img_arr = []

  for index_b in range(28):
    for index_a in range(28):
      pix_l = img_pix[index_a, index_b][3]/255
      img_arr.append(pix_l)

  # num = test_image(img_arr)
  run_tf()
  num = 'na'

  return jsonify(ok=1, num=num)


if __name__ == '__main__':
  app.run()
