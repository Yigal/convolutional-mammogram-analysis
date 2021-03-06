#  Copyright 2015-present The Scikit Flow Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
This example showcases how simple it is to build image classification networks.
It follows description from this TensorFlow tutorial:
    https://www.tensorflow.org/versions/master/tutorials/mnist/pros/index.html#deep-mnist-for-experts
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from sklearn import metrics
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import skflow
import readMammograms

### Download and load MNIST data.

mgrams = readMammograms.readData()
mnist = input_data.read_data_sets('MNIST_data')
print(type(mnist.train.images))
print(type(mnist.train.images[0]))
# print(len(mnist.train.images))
# print(mnist.train.images[0])
# print(len(mnist.train.images[0]))
print(mnist.test.labels)

print(type(mnist.train.labels[0]))

mgrams = readMammograms.readData()
# print(type(mgrams.data))
# print((mgrams.labels[0]))

# print(mgrams.labels[50])

### Linear classifier.

# classifier = skflow.TensorFlowLinearClassifier(
#     n_classes=10, batch_size=100, steps=1000, learning_rate=0.01)
# classifier.fit(mnist.train.images, mnist.train.labels)
# score = metrics.accuracy_score(mnist.test.labels, classifier.predict(mnist.test.images))
# print('Accuracy: {0:f}'.format(score))

### Convolutional network

def max_pool_2x2(tensor_in):
    return tf.nn.max_pool(tensor_in, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1],
        padding='SAME')

def conv_model(X, y):
    # reshape X to 4d tensor with 2nd and 3rd dimensions being image width and height
    # final dimension being the number of color channels
    X = tf.reshape(X, [-1, 1024, 1024, 1])
    # first conv layer will compute 32 features for each 5x5 patch
    with tf.variable_scope('conv_layer1'):
        h_conv1 = skflow.ops.conv2d(X, n_filters=32, filter_shape=[5, 5],
                                    bias=True, activation=tf.nn.relu)
        h_pool1 = max_pool_2x2(h_conv1)
    # second conv layer will compute 64 features for each 5x5 patch
    with tf.variable_scope('conv_layer2'):
        h_conv2 = skflow.ops.conv2d(h_pool1, n_filters=64, filter_shape=[5, 5],
                                    bias=True, activation=tf.nn.relu)
        h_pool2 = max_pool_2x2(h_conv2)
        # reshape tensor into a batch of vectors
        h_pool2_flat = tf.reshape(h_pool2, [-1, 1024 * 1024 * 64])
    # densely connected layer with 1024 neurons
    # h_fc1 = skflow.ops.dnn(h_pool2_flat, [1024], activation=tf.nn.relu, dropout=0.5)
    h_fc1 = skflow.ops.dnn(h_pool2_flat, [1024], activation=tf.nn.relu)
    return skflow.models.logistic_regression(h_fc1, y)

# Training and predicting
classifier = skflow.TensorFlowEstimator(
    model_fn=conv_model, n_classes=3, steps=1000, #number of steps
    learning_rate=0.001)
classifier.fit(mgrams.data, mgrams.labels)
score = metrics.accuracy_score(mgrams.labels, classifier.predict(mgrams.data))
print('Accuracy: {0:f}'.format(score))
