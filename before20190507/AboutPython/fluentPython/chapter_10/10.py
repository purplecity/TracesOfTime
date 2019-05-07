# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/2/6 9:54 AM                               
#  Author           purplecity                                       
#  Name             10.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

from array import array
import reprlib

a = array("d",[3,4,5])

a = reprlib.repr(a)
x = a[a.find('['):-1]
print(x)

b=[1,2,3]
print(b[-1])
print(b[1:-1])


#不建议只为了避免创建实例属性而使用 __slots__ 属性。__slots__ 属性只应该用于节省内存，而且仅当内存严重不足时才应该这么做。

'''

但
是需要一些特殊的实用函数协助。其中一个是内置的 zip 函数。使
用 zip 函数能轻松地并行迭代两个或更多可迭代对象，它返回的元
组可以拆包成变量，分别对应各个并行输入中的一个元素. 跟emuerate对应

something notice:
>>> list(zip(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3])) # ➌
[(0, 'A', 0.0), (1, 'B', 1.1), (2, 'C', 2.2)]  并没报错
>>> from itertools import zip_longest # ➍
>>> list(zip_longest(range(3), 'ABC', [0.0, 1.1, 2.2, 3.3], fillvalue=-1))
[(0, 'A', 0.0), (1, 'B', 1.1), (2, 'C', 2.2), (-1, -1, 3.3)]



'''