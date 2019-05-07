# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/7 10:03 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_9.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 你想创建一个新的拥有一些额外功能的实例属性类型，比如类型检查。
# 其实就是之前的回顾，只不过描述器不能为每个实例单独定义
'''
# Does NOT work
class Point:
    def __init__(self, x, y):
        self.x = Integer('x') # No! Must be a class variable
        self.y = Integer('y')
        self.x = x
        self.y = y
'''

'''

# 类装饰器

@decorator
class C: ...
x=C(99)

class C: ...
C=decorator(C)
x=C(99)

 x=C(99) <==> decortor(C)(99)

'''

class Typed:
    def __init__(self,name,expected_type):
        self.name=name
        self.expected_type=expected_type

    def __get__(self,instance,cls):
        if instance is None:
            return self
        else:
            return instance.__dict__[self.name]
    def __set__(self, instance, value):
        if not isinstance(value,self.expected_type):
            raise TypeError('Expected'+str(self.expected_type))
        instance.__dict__[self.name]=value

    def __delete__(self, instance):
        del instance.__dict__[self.name]


def typeassert(**kwargs):
    def decorate(cls):
        for name,expected_type in kwargs.items():
            setattr(cls,name,Typed(name,expected_type))
        return cls
    return decorate

@typeassert(name=str,shares=int,price=float)
class Stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price

#如果x=Stock。 返回一个Stock实例。在return cls一处。 然后就加了个name，shares，price三个属性的get set del方法
'''
def setattr(x, y, v): # real signature unknown; restored from __doc__
    """
    Sets the named attribute on the given object to the specified value.
    
    setattr(x, 'y', v) is equivalent to ``x.y = v''
'''

#到此位置就是通过描述器给类的属性加上一些方法的属性。是通过描述器来的。而且是通过装饰器来的。
#而且是通过一个描述符类来个三个属性都添加上方法。