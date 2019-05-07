# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/1/25 5:29 PM                               
#  Author           purplecity                                       
#  Name             5.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
'''
#python中用的多还是协程(生成器yield等)装饰器闭包。元类还是用处不大不实用也不知道干嘛的。只知道是生成类的。

def  test():
    slice
    ...

print(test.__doc__)


# lambda就是创建匿名函数。 lambda 参数:表达式  返回函数对象。
addtest = lambda a: a+1
print(addtest(2))
print(callable(addtest)) #检测是否可调用

# 调用类时会运行类的 __new__ 方法创建一个实例，然后运行
# __init__ 方法，初始化实例，最后把实例返回给调用方。因为 Python
# 没有 new 运算符，所以调用类相当于调用函数。（通常，调用类会创建
# 那个类的实例，不过覆盖 __new__ 方法的话，也可能出现其他行为。


#这一章到现在就是一个lambda和可调用对象的收获。
#不仅 Python 函数是真正的对象，任何 Python 对象都可以表现得像函
#数。为此，只需实现实例方法 __call__。


import random

class BingoCage:
    def __init__(self,items):
        self.__items  = list(items)
        random.shuffle(self.__items)

    def pick(self):
        try:
            return self.__items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
    def __call__(self):
        return self.pick()

#bingo.pick() 的快捷方式是 bingo()。

# 重温dir __dict__ dir()函数返回的是一个list。包括父属性。 而且实例跟类以及函数的属性也是有区别的，这个要实验以前实验过但是觉得没多大必要。而且比较复杂。只有super函数的时候用来检验
super虽然知道概念了。但还是有不懂的地方。cookbook中supper能玩死人
'''

def tag(name,*content,cls=None,**atrs):
    print("name:",name)
    print("content:",content)
    print("cls:",cls)
    print("atrs:",atrs)
    print("-----end-----")


tag("br")
tag("p","hello")
tag("p","hello","world")
tag('p', 'hello', id=33)
tag('p', 'hello', 'world', cls='sidebar')
tag(content='testing', name="img")
my_tag = {'name': 'img', 'title': 'Sunset Boulevard','src': 'sunset.jpg', 'cls': 'framed'}
tag(**my_tag)

#总结 普通参数可以用关键字参数传递。关键字参数只能用关键字参数传递

# 接下来就是三个模块的使用 inspect  operator functools
import inspect
import operator
import functools

#itemgetter(1) 的作用与 lambda fields: fields[1]
# attrgetter就是获取属性。

#functools.partial 这个高阶函数用于部分应用一个函数。部分应用
#是指，基于一个函数创建一个新的可调用对象，把原函数的某些参数固定
