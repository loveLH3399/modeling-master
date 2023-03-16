#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 10:52:51 2020

@author: tom verguts
several linear cuts in 2D space
convenient to make slides illustrating how backprop works
"""

import matplotlib.pyplot as plt
import numpy as np # x和y值通过numpy中的linspace函数生成，它们在指定的范围内生成一系列均匀分布的数值

w = np.array([[1, 1, 0], [2, -1, 2], [-1.5, 2, 3], [-1, -1, -1]]) # 数组"w"实际上是一个4x3的矩阵（或二维数组），其中每一行是一个向量，表示一个线性切面的系数。具体来说，每个向量包含三个元素，前两个元素是该切面方程中x和y变量的系数，第三个元素是常数项。
fig, axs = plt.subplots(nrows = 2, ncols = 2)

x = np.linspace(-1, 1)

for loop in range(4): # 代码中的for循环通过遍历数组“w”的每一行，生成对应的x和y值，并使用pyplot的plot函数将它们绘制在图形上。
	row = loop//2
	col = loop%2
	y = w[loop, 0]*x + w[loop, 1]
	axs[row, col].plot(x, y, color = "black")
	axs[row, col].set_xlim(left = -1, right = 1)
	axs[row, col].set_ylim(bottom = -1, top = 1)
