# 过滤序列元素

#最简单的就是列表生成式。缺点是可能内存占用过大。不如生成器保存一个算法。
mylist = [1, 4, -5, 10, -7, 2, 3, -1]
#[ n for n in mylist if n > 0 ]
pos = (n for n in mylist if n > 0 )
for x in pos:
    print(x)


# 如果过滤规则比较复杂就放到函数里面
import math
values = ['1', '2', '-3', '-', '4', 'N/A', '5']

def is_int(val):
    try:
        x=int(val)
        return True
    except ValueError:
        return False
print( type(filter(is_int,values) ) )  #<class 'filter'> filter() 函数创建了一个迭代器，因此如果你想得到一个列表的话,要用list去转换
print(list(  filter( is_int,values  )   ))  #['1', '2', '-3', '4', '5']

mylist = [1, 4, -5, 10, -7, 2, 3, -1]
# 过滤的时候转换数据

print([math.sqrt(x) for x in mylist if x > 0 ])

#过滤的时候用新数据代替而不是丢弃
print([math.sqrt(x) if x > 0 else 0 for x in mylist ])
'''
[1.0, 2.0, 3.1622776601683795, 1.4142135623730951, 1.7320508075688772]
[1.0, 2.0, 0, 3.1622776601683795, 0, 1.4142135623730951, 1.7320508075688772, 0]
'''

# 用另外一个相关联的序列来过滤某个序列的时候
# itertools.compress() ， 它以一个 iterable 对象和一个相对应的 Boolean 选择器序列作为输入参数。 然后输出 iterable 对象中对应选择器为 True 的元素。
# compress返回的也是一个迭代器要得到一个列表的话要用list去转换


addresses = [
    '5412 N CLARK',
    '5148 N CLARK',
    '5800 E 58TH',
    '2122 N CLARK',
    '5645 N RAVENSWOOD',
    '1060 W ADDISON',
    '4801 N BROADWAY',
    '1039 W GRANVILLE',
]
counts = [ 0, 3, 10, 4, 1, 7, 6, 1]
from itertools import compress
more5=[ n > 5 for n in counts ]
print(type(more5),more5)
print( type(compress(addresses,more5)), list(compress(addresses,more5)) )

'''
<class 'list'> [False, False, True, False, False, True, True, False]
<class 'itertools.compress'> ['5800 E 58TH', '1060 W ADDISON', '4801 N BROADWAY']
'''



