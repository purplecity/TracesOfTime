# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/8 11:59 AM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_10.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


#有意思值得看，意犹未尽
#  你想将一个只读属性定义成一个property，并且只在访问的时候才会计算结果。 但是一旦被访问后，你希望结果值被缓存起来，不用每次都去计算。

#定义一个延迟属性的一种高效方法是通过使用一个描述器类

class lazyproperty:
    def __init__(self,func):
        self.func=func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value=self.func(instance)
            setattr(instance,self.func.__name__,value)
            return value

import math
class Circle:
    def __init__(self,radius):
        self.radius=radius

    @lazyproperty
    def area(self):
        print('computing area')
        return math.pi * self.radius ** 2

    @lazyproperty
    def perimeter(self):
        print('computing perimeter')
        return 2*math.pi * self.radius

#我觉得其实就是创建了两个类的实例。 调用area其实就是调用被描述器类装饰器装饰的实例。
'''
按照involing Descriptors中的方法，b.x的转换是
if b是个objects type(b).__dict__['x'].__get__(b,type(b))
if b是个classes b.__dict__['x'].__get__(None,b)
#总结其实就是去描述符类中的get set方法。自动触发而已。
'''

c=Circle(4.0)
print(c.__dict__)

print('----------------------')
print(dir(c))
x=dir(c)
print(type(x[-2]),type(x[-3]))  #
print('**********************')
print(c.radius)
print(vars(c))
print(c.area) #1 内部转换area=lazyproperty(area)是一个实例 #2 c.area -> c.__dict__['area'].__get__(c,class_Circle)
# instance=c,cls=Circle这个类 然后def area(c) ==> 打印打印。然后计算值。然后设置了c有def area这个函数 值为算出的值。下次在调用就直接调用dict中了area了。
# 有三处同名，1，area=lazyproperty(area) 前面实例后面函数 2 value=self.func(instance) func是area函数名 3 setattr(instance,self.func.__name__,value) 把函数名作为dict中的属性也就是名 最后area可能涉及三个名。都是同名，实例名，函数名，实例的属性名我日
# c.x的区别:x如果是一个c的属性。那么就会去c的__dict__中找。如果只是一个类的实例。并没有标记为self.x 这里x是描述符类实例所以会自动调用描述符类的__get__方法   #这些自动转换很关键。包括装饰器的自动转换area=lazyproperty(area)。包括描述符的自动转换objects type(b).__dict__['x'].__get__(b,type(b))
print(vars(c))
print(c.area)
del c.area
print(vars(c))
print(c.perimeter)
print(vars(c))
c.perimeter=25
print(vars(c))
print(c.perimeter)

'''
 每次访问属性时它的 __get__() 、__set__() 和 __delete__() 方法就会被触发。 不过，如果一个描述器仅仅只定义了一个 __get__() 方法的话，它比通常的具有更弱的绑定。 特别地，只有当被访问属性不在实例底层的字典中时 __get__() 方法才会被触发。

lazyproperty 类利用这一点，使用 __get__() 方法在实例中存储计算出来的值， 这个实例使用相同的名字作为它的property。 这样一来，结果值被存储在实例字典中并且以后就不需要再去计算这个property了。
'''
# vars dir和__dict__区别
'''
vars([object])就是返回对象__dict__的内容，无论是类对象还是实例对象

__dict__与dir()的区别：

dir()是一个函数，返回的是list；
__dict__是一个字典，键为属性名，值为属性值；
dir()用来寻找一个对象的所有属性，包括__dict__中的属性，__dict__是dir()的子集；

实例的__dict__仅存储与该实例相关的实例属性，（就是带self的变量不包含函数和不带self的变量，见下一节观察）

正是因为实例的__dict__属性，每个实例的实例属性才会互不影响。

类的__dict__存储所有实例共享的变量和函数(类属性，方法等)，类的__dict__并不包含其父类的属性。

dir()是Python提供的一个API函数，dir()函数会自动寻找一个对象的所有属性(包括从父类中继承的属性)。

'''
#意犹未尽

'''
{'radius': 4.0}
----------------------
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'area', 'perimeter', 'radius']
<class 'str'> <class 'str'>
4.0
{'radius': 4.0}
computing area
50.26548245743669
{'radius': 4.0, 'area': 50.26548245743669}
50.26548245743669
{'radius': 4.0}
computing perimeter
25.132741228718345
{'radius': 4.0, 'perimeter': 25.132741228718345}
{'radius': 4.0, 'perimeter': 25}
25
'''
# 你想将一个只读属性定义成一个property，并且只在访问的时候才会计算结果。 但是一旦被访问后，你希望结果值被缓存起来，不用每次都去计算。
# 回过头来看这句话。有self.xxx的才是类或者实例自己的属性。没有的就不是。主题是描述符类访问的时候才有值。然后保存在自己的dict中不用每次都去赋值
# 意犹未尽

#收获 对于实例来说。self.xxx才是dict中的属性。 两个自动转换很关键。包括装饰器的自动转换area=lazyproperty(area)。包括描述符的自动转换objects type(b).__dict__['x'].__get__(b,type(b))