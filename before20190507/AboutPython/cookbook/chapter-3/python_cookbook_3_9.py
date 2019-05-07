#  在大数据集(比如数组或网格)上面执行计算 NumPy库

x=[1,2,3]
y=[2,3,5]
print(x+y)  #list只有+没有- & |操作

import numpy as np

ax=np.array([1,2,3])
ay=np.array([2,3,5])
print(ax*2,ax+10,ax+ay,ax*ay,np.sqrt(ax),np.cos(ax))

grid=np.zeros(shape=(10000*10000),dtype=float) # 10000*10000的浮点网络。运算还是会作用在每一个元素上

#变黄是python的bug。是有array这个函数的.命令行可以
'''
[1, 2, 3, 2, 3, 5]
[2 4 6] [11 12 13] [3 5 8] [ 2  6 15] [1.         1.41421356 1.73205081] [ 0.54030231 -0.41614684 -0.9899925 ]
'''