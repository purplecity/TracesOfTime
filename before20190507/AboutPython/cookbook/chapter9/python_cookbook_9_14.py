# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/19 8:00 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_14.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 自动记录一个类中属性和方法定义的顺序， 然后可以利用它来做很多操作（比如序列化、映射到数据库等等）。
#元类定义了prepare以后，会最先执行prepare方法，返回一个空的定制的字典，然后再执行类的语句，类中定义的各种属性被收集入定制的字典，最后传给new和init方法

from collections import OrderedDict

class Typed:
    _expected_type=type(None)
    def __init__(self,name=None):
        self._name=name

    def __set__(self, instance, value):
        if not isinstance(value,self._expected_type):
            raise TypeError('Expected' + str(self._expected_type))
        instance.__dict__[self._name]=value


class Integer(Typed): _expected_type = int

class Float(Typed): _expected_type =  float

class String(Typed): _expected_type =  str


class OrderedMeta(type):
    def __new__(cls, clsname,bases,clsdict):
        print(cls,clsname,bases,clsdict,"&"*3)  #厉害了。这个OrderDict是Struct的OrderDict然后传给clsdict我草  clsdict并不是一个dict知识一个OrderDict对象两者形式不一样虽然调用一样。需要dict以下。打印clsdict就知道了
        d=dict(clsdict)
        order=[]
        for name,value in clsdict.items():
            if isinstance(value,Typed):
                value._name=name
                order.append(name)
        d['_order']=order
        print(d)
        #{'__module__': '__main__', '__qualname__': 'Structure', 'as_csv': <function Structure.as_csv at 0x10cbe5048>, '_order': []}
        #{'__module__': '__main__', '__qualname__': 'Stock1', 'name': <__main__.String object at 0x105fa2160>, 'shares': <__main__.Integer object at 0x105fa21d0>, 'price': <__main__.Float object at 0x105fa2208>, '__init__': <function Stock1.__init__ at 0x105fa30d0>, '_order': ['name', 'shares', 'price']}
        return type.__new__(cls,clsname,bases,d)

    @classmethod
    def __prepare__(cls, clsname, bases):  #bases父类
        print(cls,clsname,bases,"*"*3)
        return OrderedDict()

class Structure(metaclass=OrderedMeta):
    def as_csv(self):
        print(self)
        return ','.join(str(getattr(self,name)) for name in self._order)

'''
<class '__main__.OrderedMeta'> Structure () ***
<class '__main__.OrderedMeta'> Structure () OrderedDict([('__module__', '__main__'), ('__qualname__', 'Structure'), ('as_csv', <function Structure.as_csv at 0x10dc45048>)]) &&&
{'__module__': '__main__', '__qualname__': 'Structure', 'as_csv': <function Structure.as_csv at 0x10dc45048>, '_order': []}
'''


'''
>>> d1=collections.OrderedDict()
>>> d1['a'] = 'A'
>>> d1['b'] = 'B'
>>> print(d1)
OrderedDict([('a', 'A'), ('b', 'B')])
>>> d2=dict()
>>> d2['a']='A'
>>> d2['b']="B"
>>> print(d2)
{'a': 'A', 'b': 'B'}
>>> 
'''

'''
class Stock(Structure):
    x=String()
    y=Integer()
    z=Float()

    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price

print(Stock.__dict__)  #有x,y,z三个实例 和init函数
print(dir(Stock))   #有x,y,z 三个实例 和init 函数

s = Stock('GOOG',100,490.1)
print(s.__dict__)  #只有三个属性值  {'name': 'GOOG', 'shares': 100, 'price': 490.1}
print(dir(s))  #有x,y,z三个实例值和name shares price三个属性值
print(s.x)  #<__main__.String object at 0x110363128>
'''

print('^'*20)
class Stock1(Structure):
    name=String()
    shares=Integer()
    price=Float()

    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price


'''
<class '__main__.OrderedMeta'> Stock1 (<class '__main__.Structure'>,) ***
<class '__main__.OrderedMeta'> Stock1 (<class '__main__.Structure'>,) OrderedDict([('__module__', '__main__'), ('__qualname__', 'Stock1'), ('name', <__main__.String object at 0x105fa2160>), ('shares', <__main__.Integer object at 0x105fa21d0>), ('price', <__main__.Float object at 0x105fa2208>), ('__init__', <function Stock1.__init__ at 0x105fa30d0>)]) &&&
{'__module__': '__main__', '__qualname__': 'Stock1', 'name': <__main__.String object at 0x105fa2160>, 'shares': <__main__.Integer object at 0x105fa21d0>, 'price': <__main__.Float object at 0x105fa2208>, '__init__': <function Stock1.__init__ at 0x105fa30d0>, '_order': ['name', 'shares', 'price']}
'''

s1=Stock1('GOOG',100,490.1)

print(s1.as_csv())

'''
print(Stock1.__dict__)
print(dir(Stock1))
s1=Stock1('GOOG',100,490.1)
print(s1.__dict__)
print(dir(s1))  #只有属性值没有实例值 毕竟经过init覆盖了同名
print(s1.name)  #GOOG  会覆盖。

print(s1.as_csv())
'''

#<__main__.Stock1 object at 0x109bc0208>
#GOOG,100,490.1  #卧槽这里就是同名的用处。我日。真是醉了。利用prepare把name shares price的实例属性在字典中的key  放到类的属性中。然后实例就可以去掉的时候刚好等于init中的对应的东西我日。饶了一个这么大弯有必要吗吐血


'''
我们通常会看到下面这种方式定义的类：

class Stock(Model):
    name = String()
    shares = Integer()
    price = Float()
在框架底层，我们必须捕获定义的顺序来将对象映射到元组或数据库表中的行（就类似于上面例子中的 as_csv() 的功能）

确实常见但是as_csv中不是可以用self.__dict__不就可以了吗。默认是有序的了。但是这章确实有序的。因为OrderDict把Structure或者Stock1的属性顺序依次记录了

'''


print("@"*20)

#防止类中重复定义

class NoDupOrderedDict(OrderedDict):
    def __init__(self,clsname):
        self.clsname=clsname
        print(clsname,"***")
        super().__init__()

    def __setitem__(self, key, value):
        if key in self:
            raise TypeError('{} already defined in {}'.format(key, self.clsname))

        super().__setitem__(key,value)



class OrderedMeta1(type):

    def __new__(cls, clsname,bases,clsdict):
        print(clsname,bases,clsdict,"&"*5)
        d=dict(clsdict)
        d['_order'] = [name for name in clsdict if name[0] != '_']
        print(d)
        return type.__new__(cls,clsname,bases,d)

    @classmethod
    def __prepare__(metacls, name, bases):
        return NoDupOrderedDict(metacls)


class A(metaclass=OrderedMeta1):
    def spam(self): pass
    #def spam(selfs): pass   之所以去重还是因为prepare会把要创建的属性一个一个放到OrderedDict中去记录