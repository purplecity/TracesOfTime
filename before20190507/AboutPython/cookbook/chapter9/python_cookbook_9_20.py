# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/22 3:17 PM
#  Author           purplecity
#  Name             python_cookbook_9_20.py
#  Description
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 函数注解实现方法重载
'''  目的就是达到这个效果。 注解不同就重载
class Spam:
    def bar(self, x:int, y:int):
        print('Bar 1:', x, y)

    def bar(self, s:str, n:int = 0):
        print('Bar 2:', s, n)

s = Spam()
s.bar(2, 3) # Prints Bar 1: 2 3
s.bar('hello') # Prints Bar 2: hello 0
'''

'''
import inspect,types

class MultiMethod:
    def __init__(self,name):
        self._methods={}  # int: int相关的func类似于这种
        self.__name__=name

    def register(self,meth):
        sig=inspect.signature(meth)
        types=[]
        for name,parm in sig.parameters.items():
            print(name,parm,111)
            print(parm.annotation,222)
            print(parm.default,333)
            if name == "self": continue
            if parm.annotation is inspect.Parameter.empty:
                raise TypeError('Argument {} must be annotated with a type'.format(name))

            if not isinstance(parm.annotation,type):
                raise TypeError( 'Argument {} annotation must be a type'.format(name))

            if parm.default is not inspect.Parameter.empty:
                self._methods[tuple(types)] = meth  #tuple当做key?????????
            types.append(parm.annotation)
            self._methods[tuple(types)] = meth
            print(self._methods,444)


    def __call__(self, *args):
        types=tuple(type(arg) for arg in args[1:])
        meth=self._methods.get(types,None)
        if meth:
            return meth(*args)
        else:
            raise TypeError('No matching method for types {}'.format(types))

    def __get__(self, instance, cls):
        if instance is not None:
            return types.MethodType(self,instance)  # return self.instance   self.instance()
        else:
            return self

#2 types.MethodType() 因为方法也是一个属性，所以，它也可以动态地添加到实例上，只是需要用 types.MethodType() 把一个函数变


class MultiDict(dict):
    def __setitem__(self, key, value):
        print(self,"^^"*3)  #这个prepare方法还是一个一个传进去的吗我草。显然module qualname 第一bar都是走最后的else。然后第二bar走这里
        if key in self:
            current_value=self[key]
            if isinstance(current_value,MultiMethod):
                current_value.register(value)
            else:
                mvalue=MultiMethod(key)  # multimethod object bar
                print(current_value,"%"*6)  #<function Spam.bar at 0x10d4fb510> %%%%%%
                mvalue.register(current_value)
                mvalue.register(value)
                super().__setitem__(key,mvalue)  #同样的key。
        else:
            super().__setitem__(key,value)


class MultipleMeta(type):
    def __new__(cls,clsname,bases,clsdict):
        print("&"*5,clsdict)
        return type.__new__(cls,clsname,bases,dict(clsdict))

    @classmethod
    def __prepare__(metacls, name, bases):
        return MultiDict()

class Spam(metaclass=MultipleMeta):
    def bar(self, x: int, y: int):
        print('Bar 1:', x, y)

    def bar(self, s: str, n: int = 0):
        print('Bar 2:', s, n)

'''
'''
{} ^^^^^^
{'__module__': '__main__'} ^^^^^^
{'__module__': '__main__', '__qualname__': 'Spam'} ^^^^^^
{'__module__': '__main__', '__qualname__': 'Spam', 'bar': <function Spam.bar at 0x10777b510>} ^^^^^^
self self
<class 'inspect._empty'>
<class 'inspect._empty'>
x x:int
<class 'int'>
<class 'inspect._empty'>
y y:int
<class 'int'>
<class 'inspect._empty'>
self self
<class 'inspect._empty'>
<class 'inspect._empty'>
s s:str
<class 'str'>
<class 'inspect._empty'>
n n:int=0
<class 'int'>
0
&&&&& {'__module__': '__main__', '__qualname__': 'Spam', 'bar': <__main__.MultiMethod object at 0x1076d1fd0>}
'''




'''
import time
class Date(metaclass=MultipleMeta):
    def __init__(self,year:int,month:int,day:int):
        self.year=year
        self.month=month
        self.day=day

    def __init__(self):
        t=time.localtime()
        self.__init__(t.tm_year,t.tm_mon,t.tm_mday)
'''


'''

self self
<class 'inspect._empty'>
<class 'inspect._empty'>
x x:int
<class 'int'>
<class 'inspect._empty'>
y y:int
<class 'int'>
<class 'inspect._empty'>
self self
<class 'inspect._empty'>
<class 'inspect._empty'>
s s:str
<class 'str'>
<class 'inspect._empty'>
n n:int=0
<class 'int'>
0
self self
<class 'inspect._empty'>
<class 'inspect._empty'>
year year:int
<class 'int'>
<class 'inspect._empty'>
month month:int
<class 'int'>
<class 'inspect._empty'>
day day:int
<class 'int'>
<class 'inspect._empty'>
self self
<class 'inspect._empty'>
<class 'inspect._empty'>
'''


#最后作者来了一句不应该使用方法重载。就奸恶an使用不同名称的方法就行了 其实还是不知道prepare的具体操作。MultiMethod到时挺简单的
# 算了还真不如装饰器

import types
class multimethod:
    def __init__(self,func):
        self._method={}
        self.__name__=func.__name__
        self._default=func


    def match(self,*types):
        def register(func):
            ndefaults=len(func.__defaults__) if func.__defaults__ else 0
            for n in range(ndefaults + 1):
                self._method[types[:len(types) - n ]] =func
            print(self._method)
            return self

        return register

    def __call__(self,*args):
        types=tuple(type(arg) for arg in args[1:])
        print(self._method)
        print(*types,666)
        meth=self._method.get(types,None)
        print(meth,"555")
        if meth:
            return meth(*args)
        else:
            return self._default(*args)

    def __get__(self,instance,cls):
        if instance is not None:
            print("111")
            print(self,instance,cls)
            return types.MethodType(self,instance)  #去你麻痹  self 和instance都是实例。绑定个鸡儿我日。__get__方法肯定要有。但是回事这样？

        else:
            print("222")
            return self


class Spam:

    @multimethod
    def bar(self,*args):
        raise TypeError('No matching method for bar')

    @bar.match(int, int)
    def bar(self, x, y):
        print('Bar 1:', x, y)

    @bar.match(str, int)
    def bar(self, s, n = 0):
        print('Bar 2:', s, n)

print(dir(multimethod),333)  #还真没有__get__方法我草
s = Spam()
s.bar(2, 3)
'''
按照involing Descriptors中的方法，b.x的转换是
if b是个objects type(b).__dict__['x'].__get__(b,type(b))
if b是个classes b.__dict__['x'].__get__(None,b)


'''



print(Spam.__dict__)  #'bar': <__main__.multimethod object at 0x1031d2c50>