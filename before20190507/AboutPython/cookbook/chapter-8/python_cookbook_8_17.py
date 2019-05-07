# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/14 3:33 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_17.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#创建不调用init方法的实例  #__new__
'''
class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day
'''
#查看python学习手册元类那一张
'''
在Python 3.0 中，用户定义的类对象是名为t y p e的对象的实例，t y p e本身是一个
类。

t y p e内置函数返回任何对象的类型（它本身是一个对象）。对于列表这样的
内置类型，实例的类型是一个内置的列表类型，但是，列表类型的类型是类型t y p e自
身——顶层的t y p e对象创建了具体的类型，具体的类型创建了实例。你将会在交互提示
模式中亲自看到这点。例如，在Python 3.0中：
C:\misc> c:\python30\python
>>> type([]) # In 3.0 list is instance of list type
<class 'list'>
>>> type(type([])) # Type of list is type class
<class 'type'>
>>> type(list) # Same, but with type names
<class 'type'>
>>> type(type) # Type of type is type: top of hierarchy
<class 'type'>

Python 3.0中，“类型”的概念与“类”的概念合并了。实际上，这两者基本上是同义
词——类是类型，类型也是类。即：
类型由派生自type的类定义。
用户定义的类是类型类的实例。
用户定义的类是产生它们自己的实例的类型

C:\misc> c:\python30\python
>>> class C: pass # 3.0 class object (new-style)
...
>>> X = C() # Class instance object
>>> type(X) # Instance is instance of class
<class '__main__.C'>
>>> X.__class__ # Instance's class
<class '__main__.C'>
>>> type(C) # Class is instance of type
<class 'type'>
>>> C.__class__



type是产生用户定义的类的一个类。
元类是type类的一个子类。
类对象是type类的一个实例，或一个子类。
实例对象产生自一个类。


我们已经学习过，当Python遇到一条c l a s s语句，它会运行其嵌套的代码块以创建其属
性——所有在嵌套代码块的顶层分配的名称都产生结果的类对象中的属性。这些名称通
常是嵌套的d e f所创建的方法函数，但是，它们也可以是分配来创建由所有实例共享的
类数据的任意属性。
从技术上讲，Python遵从一个标准的协议来使这发生：在一条class语句的末尾，并且在
运行了一个命名控件词典中的所有嵌套代码之后，它调用type对象来创建class对象：
class = type(classname, superclasses, attributedict)
t y p e对象反过来定义了一个__c a l l__运算符重载方法，当调用type对象的时候，该方法
运行两个其他的方法：
type.__new__(typeclass, classname, superclasses, attributedict)
type.__init__(class, classname, superclasses, attributedict)
__n e w__方法创建并返回了新的c l a s s对象，并且随后__i n i t__方法初始化了新创建的对
象。正如我们稍后将看到的，这是type的元类子类通常用来定制类的钩子。
例如，给定一个如下所示的类定义：
class Spam(Eggs): # Inherits from Eggs
data = 1 # Class data attribute
def meth(self, arg): # Class method attribute
pass

Python将会从内部运行嵌套的代码块来创建该类的两个属性（d a t a和m e t h），然后在
class语句的末尾调用type对象，产生class对象：
Spam = type('Spam', (Eggs,), {'data': 1, 'meth': meth, '__module__': '__main__'})
由于这个调用在c l a s s语句的末尾进行，它是用来扩展或处理一个类的、理想的钩子。
技巧在于，用将要拦截这个调用的一个定制子类来替代类型，下一节将展示如何做到这
一点。

__new__至少要有一个参数cls，代表要实例化的类，此参数在实例化时由Python解释器自动提供

__new__必须要有返回值，返回实例化出来的实例，这点在自己实现__new__时要特别注意，可以return父类__new__出来的实例，或者直接是object的__new__出来的实例

__init__有一个参数self，就是这个__new__返回的实例，__init__在__new__的基础上可以完成一些其它初始化的动作，__init__不需要返回值

若__new__没有正确返回当前类cls的实例，那__init__是不会被调用的，即使是父类的实例也不行

'''
'''
print(type(Date))  #<class 'type'>

d=Date.__new__(Date)  #__new__至少要有一个参数cls，代表要实例化的类 这里就是Date就是cls你要初始化新对象
# print(d.year)  #'Date' object has no attribute   Date实例的属性year还不存在，所以你需要手动初始化

data={'year':2012,'month':8,'day':29}
for key,value in data.items():
    setattr(d,key,value)
print(d.year)  #2012

'''
'''

import time

class Date:
    """方法一：使用类方法"""
    # Primary constructor
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # Alternate constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)
a = Date(2012, 12, 21) # Primary
b = Date.today() # Alternate
比较下面的方法。这个是直接参数是cls（默认是就是当前类）然后return cls的实例
'''

from time import localtime

class Date:
    def __init__(self,year,month,day):
        self.year=year
        self.month=month
        self.day=day

    @classmethod
    def today(cls):
        d=cls.__new__(cls)  #创建类实例。不会调用init
        print(d.__dict__) #{}
        print(dir(d))  #包含__setattr__   所以下面才能为所欲为的赋值
        #print(d.year)  #'Date' object has no attribute 'year'
        t=localtime()
        d.year=t.tm_year
        d.month=t.tm_mon
        d.day=t.tm_mday #显然这三个如果不是year month  day的话必须要用到__setattr__方法。否则别轻易访问底层字典
        print(d.year) #2018
        d.xx=6
        print(d.__dict__,d.xx)  #{'year': 2018, 'month': 9, 'day': 14, 'xx': 6} 6
        return d  #返回实例

x=Date.today()
#当我们在反序列对象或者实现某个类方法构造函数时需要绕过 __init__() 方法来创建对象
#反序列json对象产生额如下一个字典对象
#data = { 'year': 2012, 'month': 8, 'day': 29 }
#然后
# for key, value in data.items():
#    setattr(d, key, value)
