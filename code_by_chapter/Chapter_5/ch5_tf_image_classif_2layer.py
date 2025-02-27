#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 14:49:49 2020

@author: tom verguts
image classification; could a standard two-layer network solve this task...?
"""

import tensorflow as tf # CIFAR-10 dataset, which consists of 60,000 32x32 color images in 10 classes, with 6,000 images per class
import numpy as np
import matplotlib.pyplot as plt

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data() # load the CIFAR-10 dataset


# for plotting
fig, axes = plt.subplots(1, 4, figsize=(7,3))
for img, label, ax in zip(x_train[:4], y_train[:4], axes):
    ax.set_title(label)
    ax.imshow(img)
    ax.axis("off")
plt.show()

# pre-processing
n_labels = int(np.max(y_train)+1) # 计算数据有多少标签
image_size = x_train.shape[1]*x_train.shape[2]*x_train.shape[3]
x_train = x_train.reshape(x_train.shape[0], image_size)  / 255 # /255 得到[0,1]
x_test  = x_test.reshape(x_test.shape[0], image_size)    / 255
y_train = y_train[:,0] # remove a dimension把第1行删掉，留下第0行
y_test  = y_test[:,0] # Convert the target labels into one-hot encoded vectors使用N位状态寄存器来对N个状态进行编码，每个状态都有它独立的寄存器位，并且在任意时候，其中只有一位有效

# for piloting
x_train, y_train, x_test, y_test = x_train[:5,:], y_train[:5], x_test[:100,:], y_test[:100]

with tf.Session() as sess:
    y_train = sess.run(tf.one_hot(y_train, n_labels))
    y_test  = sess.run(tf.one_hot(y_test, n_labels))

learning_rate = 0.001
epochs = 10
batch_size = 100
batches = int(x_train.shape[0] / batch_size)
stdev = 0.001 # 学习率、迭代次数、批次大小和标准差

X   = tf.placeholder(tf.float32, [None, image_size])# X 表示输入数据的占位符，Y 表示目标标签的占位符，W 和 B 分别表示模型的权重和偏置
Y   = tf.placeholder(tf.float32, [None, n_labels])
W   = tf.Variable(np.random.randn(image_size, n_labels).astype(np.float32)*stdev)
B   = tf.Variable(np.random.randn(n_labels).astype(np.float32))

net_in  = tf.add(tf.matmul(X, W), B) # This line performs the forward pass of the neural network by computing the weighted sum of the input features X (which is a tensor三维变量) using the weights W and adding the bias B. This operation produces a new tensor net_in which is the input to the activation function.
net_inT    = 1/(1+tf.math.exp(-net_in)) # hidden transformed : Note: this is not softmax ## input压缩在 0 和 1 之间
pred = tf.nn.softmax(net_inT) # 产生每个类别的预测概率
cost = tf.reduce_mean(-tf.reduce_sum(Y*tf.math.log(pred), axis = 1)) # 定义成本函数
opt  = tf.train.GradientDescentOptimizer(learning_rate).minimize(cost) # 梯度下降最小化成本函数
init = tf.global_variables_initializer() # 这行代码在训练过程开始之前初始化模型中使用的所有变量，如权重 W 和偏置 B

with tf.Session() as sess:
    sess.run(init)
    for epoch in range(epochs):
        for i in range(batches):
            offset = i * batch_size
            x = x_train[offset:(offset+batch_size)]
            y = y_train[offset:(offset+batch_size)]
            for (x_s, y_s) in zip(x, y):
                x_s = x_s.reshape(1,image_size)
                y_s = y_s.reshape(1,n_labels)
                sess.run(opt, feed_dict= {X: x_s, Y: y_s})
        if not epoch % 5:
            for loop in range(2):
                if loop == 0:
                    data_x, data_y = x_train, y_train
                else:
                    data_x, data_y = x_test, y_test
                c = sess.run(cost, feed_dict={X: data_x, Y: data_y})
                correct_pred = tf.equal(tf.math.argmax(pred, 1), tf.math.argmax(Y, 1))
                accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))
                acc = accuracy.eval({X: data_x, Y: data_y})
                print("{} cost= {:.2f}, accuracy= {:.2f}".format(["train", "test"][loop], c, acc))        
            print("\n")   
