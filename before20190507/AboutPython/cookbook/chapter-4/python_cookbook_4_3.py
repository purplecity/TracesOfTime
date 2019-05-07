# 生成器于迭代的关系。早就知道了。
# 生成器就是迭代器也是可迭代对象。有next方法。用for或者next都可以ok。

def frange(start, stop, increment):
    x = start
    while x < stop:
        yield x
        x += increment

a=frange(1,5,0.5)
from collections import Iterable,Iterator
print(isinstance(a,Iterator),isinstance(a,Iterable))
# True True