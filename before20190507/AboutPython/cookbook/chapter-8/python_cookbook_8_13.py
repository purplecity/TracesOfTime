# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/8 5:32 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_13.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 多继承。装饰器，描述器，元类。但是最后既然推崇装饰器那么就只装饰器把。毕竟元类在下一章还得学这里也不推崇。能不用多继承就别用多继承把诶虽然无非也就是dir和dict的事
# 突然觉得前面两张实在太重要了探索清楚的话
class Descriptor:
    def __init__(self,name=None,**ops):
        self.name=name
        for key,value in ops.items():
            setattr(self,key,value)

    def __set__(self, instance, value):
        instance.__dict__[self.name]=value

'''
#如果没有就用父类的init
class Typed(Descriptor):
    expected_type=type(None)

    def __set__(self, instance, value):
        if not isinstance(value,self.expected_type):
            raise TypeError('expected'+str(self.expected_type))

        super().__set__(instance,value)

class Unsigned(Descriptor):
    def __set__(self, instance, value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super().__set__(instance,value)


class MaxSized(Descriptor):
    def __init__(self,name=None,**opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super().__init__(name,**opts)

    def __set__(self,instance,value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super().__set__(instance,value)

'''

def Typed(expected_type,cls=None):
    if  cls is None:
        return lambda cls:  Typed(expected_type,cls)

    super_set=cls.__set__

    def __set__(self,instance,value):
        if not instance(value,expected_type):
            raise TypeError('expected' + str(expected_type))
        super_set(self.instance,value)
    cls.__set__=__set__
    return cls


def Unsigned(cls):
    super_set=cls.__set__

    def __set__(self,instance,value):
        if value < 0:
            raise ValueError('Expected >= 0')
        super_set(self,instance,value)

    cls.__set__==__set__
    return cls

def MaxSized(cls):
    super_init=cls.__init__

    def __init__(self,name=None,**opts):
        if 'size' not in opts:
            raise TypeError('missing size option')
        super_init(self,name,**opts)

    cls.__init__=__init__

    super_set=cls.__set__

    def __set__(self,instance,value):
        if len(value) >= self.size:
            raise ValueError('size must be < ' + str(self.size))
        super_set(self,instance,value)

    cls.__set__=__set__
    return cls

@Typed(int)
class Integer(Descriptor): pass

@Unsigned
class UnsignedInteger(Integer): pass   #这种传递的装饰器的应用还真是意犹未尽啊.装饰再装饰

#


@Typed(float)
class Float(Descriptor):
    pass


@Unsigned
class UnsignedFloat(Float):
    pass


@Typed(str)
class String(Descriptor):
    pass


@MaxSized
class SizedString(String):
    pass

'''
class Stock:
    name=SizedString('name',size=8)   #name是给String类初始化的。size是给SizeString初始化的
    # 这里装饰器返回一个类。然后name=SizeString(‘name’,size=8)调用init函数初始化了SizeString实例。

'''

def check_attributes(**kwargs):
    def decorate(cls):
        for key,value in kwargs.items():
            if isinstance(value,Descriptor):
                value.name=key  #实例.name=str(key) ???  会触发__set__方法。有点复杂。
                setattr(cls,key,value)
            else:
                setattr(cls,key,value(key))
            return cls  #返回三个类的实例？
    return decorate

@check_attributes(name=SizedString(size=8),shares=UnsignedInteger(7),price=UnsignedFloat(0.03))

class Stock:
    def __init__(self,name,shares,price):
        self.name=name
        self.shares=shares
        self.price=price


s=Stock("pc",35,0.01)
print(s.name.name)
print(s.shares.name)
print(s.price.name)
# 我觉得很不同


#我觉得有点复杂。没有一起完整能跑的例子。这里只是适合体会，并不适合抄代码