# 一个序列中随机抽取若干元素，或者想生成几个随机数
import random
values=[1,2,3,4,5,6]
print(random.choice(values))
print(random.sample(values,2))
print(random.random()) #生成0-1的随机浮点数
#高斯分布，正太分布啥的以后再说