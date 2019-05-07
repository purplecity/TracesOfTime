# 精确的浮点数运算

from decimal import  Decimal,getcontext

getcontext().prec=6  #控制精度
print(Decimal('1.3')/Decimal('1.7'))
print(Decimal(1.3)/Decimal(1.7))
print(Decimal('1.3'))  #带不带单引号跟数字没啥区别
'''
0.764706
0.764706
1.3
'''

#求和的更精确运算

nums=[1.23e+18,1,-1.23e+18]
print(sum(nums))  #0.0  一个很大的数和一个很小的数相加。因为是逐个加的。为0.0

import math
math.fsum(nums)    #  1.0 所以指数这块要凡是涉及到计算的最好全部都用math中的方法

