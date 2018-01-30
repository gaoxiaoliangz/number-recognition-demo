from tensorflow.examples.tutorials.mnist import input_data

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)


for i in range(10):
  batch_xs, batch_ys = mnist.train.next_batch(1)
  print('----')
  print(batch_xs)
  print(batch_ys)
