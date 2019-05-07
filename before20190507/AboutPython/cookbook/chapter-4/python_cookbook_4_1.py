# 不用for循环遍历可迭代对象
'''
def next(iterator, default=None): # real signature unknown; restored from __doc__
    """
    next(iterator[, default])

    Return the next item from the iterator. If default is given and the iterator
    is exhausted, it is returned instead of raising StopIteration.
    """
    pass

'''

def manual_iter():
    with open('/Users/purplecity/a.txt') as f:
        try:
            while True:
                line=next(f)
                print(line)
        except StopIteration as e:
            print(e.value)

def manual_iter_2():
    with open('/Users/purplecity/a.txt') as f:
            while True:
                line = next(f,'hehe')  #第二个参数default是迭代器已经到了最末端，再调用next()函数的输出值.因为是‘hehe’，所以永远line不会None，而且一直是hehe。从而一直打印hehe
                if line is None:
                    break
                print(line)


manual_iter()
print('-------------')
#manual_iter_2()

items = [1, 2, 3]
list
#print(next(items))  #'list' object is not an iterator
it=iter(items)  #<class 'list_iterator'> 1   注意iter这个词！！！！！

'''

4、 内置iter函数作用

 

1、检查对象是否实现了__iter__方法，如果实现就调用，获取一个迭代器。

2、如果没有实现__iter__，但是有__getitem__方法，Python会创建一个迭代器，尝试按顺序从索引0开始获取元素。

3、如果尝试失败抛出TypeError异常
'''

print(type(it),next(it))


'''
pythonhello world

python2

hehe

python3

letgo

python4

None

'''



'''

1 迭代器

    迭代是指对集合元素遍历的一种方式，迭代器是可以实现对集合从前向后依次遍历的一个对象

2 可迭代对象

定义(表面理解)

表面来看，只要可以用 for...in...进行遍历的对象就是可迭代对象    

自定义可迭代对象(本质)

语法层面，如果一个对象实现了__iter__方法，那么这个对象就是可迭代对象

判断是否可以迭代：
from collections import Iterable
print(isinstance('abc',Iterable)   #True



for…in…遍历的本质就是调用对象的iter方法返回一个迭代器，然后通过这个迭代器去依次取得可迭代对象的每一个元素。Python中的内置可迭代对象用到的迭代器Python已经帮我们实现了

list.index可以取得下标。如果同时取索引和元素可以用到enumerate函数
for i,value in enumerate(list)
    print(i,value)
    

 可迭代的对象有个 __iter__ 方法，每次都实例化一个新的迭代器；而迭代器要实现 __next__ 方法，返回单个元素，此外还要实现 __iter__ 方法，返回迭代器本身
 迭代器是这样的对象：实现了无参数的 __next__ 方法，返回序列中的下一个元素；如果没有元素了，那么抛出 StopIteration 异常。 Python 中的迭代器还实现了__iter__ 方法，因此迭代器可以迭代。
 
     
理解迭代协议

Python 迭代协议要求一个 __iter__() 方法返回一个特殊的迭代器，这个迭代器实现了 __next__()　方法，并通过 StopIteration异常标识迭代完成。


可以被next()函数调用并不断返回下一个值的对象称为迭代器：Iterator。

可以使用isinstance()判断一个对象是否是Iterator对象：

from collections import Iterator
print(isinstance((x for x in range(10)),Iterator)   #True 生成器也是迭代器
生成器都是Iterator对象，但list、dict、str虽然是Iterable，却不是Iterator

把list、dict、str等Iterable变成Iterator可以使用iter()函数

总结： 迭代器Iterator __next__ next()方法不断返回下一个值，除非设置参数，不然报StopIteration错误
      可迭代对象 Iterable  __iter__方法。返回的是一个迭代器
      
      for…in…遍历的本质就是调用对象的iter方法返回一个迭代器，然后通过这个迭代器去依次取得可迭代对象的每一个元素。Python中的内置可迭代对象用到的迭代器Python已经帮我们实现了
      
      4、 内置iter函数作用

        1、检查对象是否实现了__iter__方法，如果实现就调用，获取一个迭代器。
        
        2、如果没有实现__iter__，但是有__getitem__方法，Python会创建一个迭代器，尝试按顺序从索引0开始获取元素。
        
        3、如果尝试失败抛出TypeError异常

'''





