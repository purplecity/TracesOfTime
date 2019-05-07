# 同时迭代多个序列

# 迭代长度跟参数中最短序列长度一致。

a = [1, 2, 3]
b = ['w', 'x', 'y', 'z']
for i in zip(a,b):
    print(i)

for x,y in zip(a,b):
    print(x,y)

'''
(1, 'w')
(2, 'x')
(3, 'y')
1 w
2 x
3 y

'''

# itertools.zip_longest()函数.最后一个是默认值参数。没有为None
from itertools import zip_longest
for i in zip_longest(a,b,fillvalue=0):
    print(i)

for x,y in zip_longest(a,b):
    print(x,y)

'''

(1, 'w')
(2, 'x')
(3, 'y')
(0, 'z')
1 w
2 x
3 y
None z
'''


'''
class zip(object):
    """
    zip(iter1 [,iter2 [...]]) --> zip object
    
    Return a zip object whose .__next__() method returns a tuple where
    the i-th element comes from the i-th iterable argument.  The .__next__()
    method continues until the shortest iterable in the argument sequence
    is exhausted and then it raises StopIteration.
'''

headers = ['name', 'shares', 'price']
values = ['ACME', 100, 490.1]
s=dict(zip(headers,values))

'''

    def __init__(self, seq=None, **kwargs): # known special case of dict.__init__
        """
        dict() -> new empty dictionary
        dict(mapping) -> new dictionary initialized from a mapping object's
            (key, value) pairs
        dict(iterable) -> new dictionary initialized as if via:
            d = {}
            for k, v in iterable:
                d[k] = v
        dict(**kwargs) -> new dictionary initialized with the name=value pairs
            in the keyword argument list.  For example:  dict(one=1, two=2)
        # (copied from class doc)
        """
'''

a = [1, 2, 3]
b = [10, 11, 12]
c = ['x','y','z']
for i in zip(a, b, c):
     print(i)

print(list(zip(a,b)))

'''
    def __init__(self, seq=()): # known special case of list.__init__
        """
        list() -> new empty list
        list(iterable) -> new list initialized from iterable's items
        # (copied from class doc)
        """
'''
