#展开嵌套的序列

#一个包含 yield from 语句的递归生成器来轻松解决这个问题

from collections import Iterable

def flatten(items,ignore_type=(str,bytes)):
    for x in items:
        if isinstance(x,Iterable) and not isinstance(x,ignore_type):
            yield from flatten(x)
        else:
            yield x

items = [1, 2, [3, 4, [5, 6], 7], 8]
for x in flatten(items):
    print(x)

items = ['Dave', 'Paula', ['Thomas', 'Lewis']]
for x in flatten(items):
    print(x)



