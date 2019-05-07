# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/1/25 2:39 PM                               
#  Author           purplecity                                       
#  Name             2.5.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#python默认的序列类型都是一维的。
'''
my_list = [[]] * 3 来初始化一个
由列表组成的列表，但是你得到的列表里包含的 3 个元素其实是 3
个引用，而且这 3 个引用指向的都是同一个列表。
'''

board = [["_"] * 3 for i in range(3)]
board[1][2] = "x"

err_board = [["_"]*3] * 3  #列表的元素是一个引用。引用指向["_"],["_"],["_"] 乘以3就是变为3个引用。就因为list作为元素时候存着的是引用。而不是值。乘以3就是变为3个引用
err_board[1][2] = "x"
print(board,err_board)

row = ["_"]*3
see = []
for i in range(3):
    see.append(row)

print(see)
see[2][1] = "0"
print(see)

good_see = []
for i in range(3):
    good_row = ["_"] * 3# 每次循环新创建引用
    good_see.append(good_row)

good_see[2][1] = "0"
print(good_see)


# += *=会调用__iadd__。没有这个就会调用__add__,就地加乘。__add__会得到一个新的对象会浪费内存。可变对象一般都有__iadd__   不可变对象只有__add__  str因为太频繁使用所以得地优化了下str 是一个例外，因为对字符串做 += 实在是太普遍了，所以 CPython 对它做了优化。为 str
# 初始化内存的时候，程序会为它留出额外的可扩展空间，因此进行增量操作的时候，并不会涉
# 及复制原有字符串到新位置这类操作。



## 呀 2.5 2.6确实值得一读  可变对象放在序列中其实是以引用方式存在的。


#  list.sort 方法会就地排序列表，也就是说不会把原列表复制一份。这
# 也是这个方法的返回值是 None 的原因，提醒你本方法不会新建一个列
# 表。在这种情况下返回 None 其实是 Python 的一个惯例：如果一个函数
# 或者方法对对象进行的是就地改动，那它就应该返回 None，好让调用
# 者知道传入的参数发生了变动，而且并未产生新的对象。 6666666


# 2.8  bisect.bisect bisect.insort就是查找一个排序序列  给出一个值在哪个位置(不一定是相等)。和插入之后保持排序 。对可迭代对象有效
#def grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
#... i = bisect.bisect(breakpoints, score)
#... return grades[i]
#...
#>>> [grade(score) for score in [33, 99, 77, 70, 89, 90, 100]]
#['F', 'A', 'C', 'C', 'B', 'A', 'A']

# 2.9呀 python居然还有数组类型  2.9值得一看


from array import array
from random import random
floats = array('d',(random() for i in range(10**7)))
print(floats[-1])
fp = open("/Users/purplecity/zaqizaba/222.bin","wb")
floats.tofile(fp)
fp.close()
floats2=array('d')
fp=open("/Users/purplecity/zaqizaba/222.bin","rb")
floats2.fromfile(fp,10**7)
fp.close()
print(floats2[-1])
print(floats2 == floats)

# memoryview 手术刀。精准操作。而不复制内存。高级操作
# 2.9.4