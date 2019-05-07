# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/22 11:40 AM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_18.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#types  只是提供类的名字、父类元组、关键字参数（只是关键字参数），以及一个用成员变量填充类字典的回调函数

def __init__(self,name,shares,price):
    self.name=name
    self.shares=shares
    self.price=price


def cost(self):
    return self.shares * self.price

cls_dict={
    '__init__':__init__,
    'cost':cost
}

import types
Stock=types.new_class("stock",(),{}, lambda ns: ns.update(cls_dict))
Stock.__module__=__name__  #这一句对命名有帮助
print(Stock)   #<class 'types.stock'>  <class '__main__.stock'>
print(dir(Stock))
s= Stock('ACME', 50, 91.1)
print(s.name)
#  dict.update(dict2)
# 参数
# dict2 -- 添加到指定字典dict里的字典。

# new_class() 第四个参数最神秘，它是一个用来接受类命名空间的映射对象的函数。 通常这是一个普通的字典，但是它实际上是 __prepare__() 方法返回的任意对象
## types.new_class() 第四个参数的回调函数接受 __prepare__() 方法返回的映射对象。  意味着比直接type()更详细

#如果是想由自定义的元类创建也放到第三个参数
# types.new_class() 第四个参数的回调函数接受 __prepare__() 方法返回的映射对象。

'''
import abc
Stock1=types.new_class("Stock1",(),{"metaclass":abc.ABCMeta}),lambda ns:ns.update(cls_dict)
Stock1.__module__=__name__
'''
#看到这里还真是以编程的方式定义类




# ns指的是namespace 那么namespace是一个dict类似的东东？



'''
metaclass, kwargs, ns = types.prepare_class('Stock', (), {'metaclass': type})
print(metaclass,kwargs,ns)  #<class 'type'> {} {}
'''



import operator,sys

def name_tuple(classname,fieldnames):
    cls_dict={name:property(operator.itemgetter(n)) for n,name in enumerate(fieldnames)}

    # .name的时候就会出get函数即operator.itemgetter
    #有__get__就好了。为啥要这样操作呢？

    def  __new__(cls,*args):
        if len(args) != len(fieldnames):
            raise TypeError('Expected {} arguments'.format(len(fieldnames)))
        return tuple.__new__(cls,args)

    cls_dict['__new__']=__new__  #用来实例化的

    cls=types.new_class(classname,(tuple,),{},lambda ns:ns.update(cls_dict))

    cls.__module__=sys._getframe(1).f_globals['__name__']
    return cls

Point=name_tuple("point",['x','y'])
print(Point)
p=Point(4,5)
print(type(p))
print(p,len(p))





















