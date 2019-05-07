# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/1/30 2:31 PM                               
#  Author           purplecity                                       
#  Name             8.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 可变对象的赋值是引用不会创建新对象。变量不是存储数据的盒子只是对象的标注。也就是别名

# += *=对于可变对象入dict list set来说就地操作。但是对于不可变对象tuple来说另外复制，str除外

'''
l1 = [3,[66,55,44],(7,8,9)]
l2 = list(11)
l1.append(100)
l1[1].remove(55)
print("l1:",l1)
print("l2:",l2)
l2[1] += [33,22]
l2[2] += (10,11)
print("l1:",l1)
print("l2:",l2)


def f(a,b):
    a += b
    return a

x=1
y=2

a=[1,2]
b=[3,4]

t=(10,20)
u=(30,40)

f(x,y)
f(a,b)
f(t,u)
print(x,y)
print(a,b)
print(t,u)
'''
import  weakref

'''
a_set = {0,1}
wref = weakref.ref(a_set)
print(wref)
print(wref())
a_set = {2,3,4}
print(wref())
print(wref() is None)

'''

class Cheese:
    def __init__(self,kind):
        self.kind = kind

    def __repr__(self):
        return "cheese {}".format(self.kind)



stock = weakref.WeakValueDictionary()
catalog = [Cheese("red"),Cheese("block"),Cheese("lock"),Cheese("hehe")]
for cheese in  catalog:
    stock[cheese.kind] = cheese

print(sorted(stock.keys()))
del catalog
print(sorted(stock.keys()))

'''
如果一个类需要知道所有实例，一种好的方案是创建一个
WeakSet 类型的类属性，保存实例的引用。如果使用常规的 set，实例
永远不会被垃圾回收，因为类中有实例的强引用，而类存在的时间与
Python 进程一样长，除非显式删除类。
'''
from array import array
