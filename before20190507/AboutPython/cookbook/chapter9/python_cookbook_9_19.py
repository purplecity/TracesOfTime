
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/22 2:27 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_19.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

import operator

class StructTupleMeta(type):
    def __init__(cls,*args,**kwargs):
        print(StructTupleMeta.__mro__)
        super().__init__(*args,**kwargs)
        for n,name in enumerate(cls._fields):
            setattr(cls,name,property(operator.itemgetter(n)))

class StructTuple(tuple,metaclass=StructTupleMeta):
    _fields=[]
    def __new__(cls, *args):
        if len(args) != len(cls._fields):
            raise ValueError('{} arguments required'.format(len(cls._fields)))
        print(StructTuple.__mro__)
        return super().__new__(cls,args)


class Stock(StructTuple):
    _fields = ['name','shares','price']

class Point(StructTuple):
    _fields =  ['x','y']


'''
(<class '__main__.StructTupleMeta'>, <class 'type'>, <class 'object'>)
(<class '__main__.StructTupleMeta'>, <class 'type'>, <class 'object'>)
(<class '__main__.StructTupleMeta'>, <class 'type'>, <class 'object'>)
'''

s=Stock('aceme',50,91.1)  #这里没有call方法。会用到__new__用
#  (<class '__main__.StructTuple'>, <class 'tuple'>, <class 'object'>) 当前类的下一个类的方法

print(type(s))  #<class '__main__.Stock'> 其实是元类
print(s[0])
print(dir(Stock))
print(Stock.__dict__)  #'_fields': ['name', 'shares', 'price'], '__doc__': None, 'name': <property object at 0x104e6f048>, 'shares': <property object at 0x104e6f098>, 'price': <property object at 0x104e6f0e8>}
# .号就是fget方法。 . = 就是set方法
print(dir(s))
print(s.__dict__)
#s.shares=23 #error
print(s._fields)  #['name', 'shares', 'price']


#类定义和类实例化的时候不同 牛逼啊。意犹未尽