# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/17 8:24 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_9.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 将装饰器定义为类

#你想使用一个装饰器去包装函数，但是希望返回一个可调用的实例。 你需要让你的装饰器可以同时工作在类定义的内部和外部。

# 需要__call__()  __get__()

import types
from functools import wraps

class Profiled:
    def __init__(self,func):
        wraps(func)(self)
        self.ncalls=0

    def __call__(self, *args, **kwargs):
        self.ncalls += 1
        return self.__wrapped__(*args,**kwargs)

    def __get__(self,instance,cls):
        if instance is None:
            return self

        else:
            return types.MethodType(self,instance)

@Profiled
def add(x,y): return x + y

class Spam:
    @Profiled
    def bar(self,x): print(self,x)

print(add.ncalls,add(2,3),type(add),add.__dict__)  #函数add被实例化为add实例。 调用call
print(add.ncalls,add(3,4),add.ncalls)  #1 7 2

#5 <class '__main__.Profiled'> {'__module__': '__main__', '__name__': 'add', '__qualname__': 'add', '__doc__': None, '__annotations__': {}, '__wrapped__': <function add at 0x107fd9c80>, 'ncalls': 1}

s=Spam()
print(Spam.bar.ncalls)  #0
print(dir(s),'***')
print(s.__dict__,'&&&')  #  {} &&&
print(dir(Spam))
print(Spam.__dict__,'****')  #  {'__module__': '__main__', 'bar': <__main__.Profiled object at 0x109db54e0>, '__dict__': <attribute '__dict__' of 'Spam' objects>, '__weakref__': <attribute '__weakref__' of 'Spam' objects>, '__doc__': None} ****
s.bar(1)   #<__main__.Spam object at 0x10b0fa4a8> 1
print(type(Spam.bar))  #<class '__main__.Profiled'>
print(s.bar,type(s.bar))  #<bound method Spam.bar of <__main__.Spam object at 0x106baa4a8>> <class 'method'> 。
print(Spam.bar.ncalls)  #1
print(s.bar.ncalls)  #1
x=Spam()
print(Spam.bar.ncalls)    #1
print(x.bar.ncalls)   #1
s.bar(2)
s.bar(3)
print(Spam.bar.ncalls)  #3
print(x.bar.ncalls) #3


'''
0 5 <class '__main__.Profiled'> {'__module__': '__main__', '__name__': 'add', '__qualname__': 'add', '__doc__': None, '__annotations__': {}, '__wrapped__': <function add at 0x10e5a7c80>, 'ncalls': 1}
1 7 2
0
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'bar'] ***
{} &&&
['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'bar']
{'__module__': '__main__', 'bar': <__main__.Profiled object at 0x10e5a34e0>, '__dict__': <attribute '__dict__' of 'Spam' objects>, '__weakref__': <attribute '__weakref__' of 'Spam' objects>, '__doc__': None} ****
<__main__.Spam object at 0x10e5a3588> 1
<class '__main__.Profiled'>
<bound method Spam.bar of <__main__.Spam object at 0x10e5a3588>> <class 'method'>
1
1
1
1
<__main__.Spam object at 0x10e5a3588> 2
<__main__.Spam object at 0x10e5a3588> 3

3
3

'''
# 并不是实例化的时候才调用__call__。 是add在调用实际参数的时候。才会调用call


#  print(s.bar.ncalls)   print(s.bar,type(s.bar))  #<bound method Spam.bar of <__main__.Spam object at 0x106baa4a8>> <class 'method'>这两个矛盾啊！！！！  按照描述符的转化逻辑，应该是Types.MethodType()返回了一个函数。 但又跟最后能调用ncalls有点不太合理毕竟能调用ncalls应该是个实例。但这个函数确实是返回函数的作为绑定函数使用


# add(1,2) 应该是实例调用call 然后传参  s.bar应该是实例然后调用call 然后传参。  这里太容易混淆了。等流畅的Python再说

'''
按照involing Descriptors中的方法，b.x的转换是
if b是个objects type(b).__dict__['x'].__get__(b,type(b))
if b是个classes b.__dict__['x'].__get__(None,b)
#总结其实就是去描述符类中的get set方法。自动触发而已。

可见自定义__get__方法是一定要cls参数的

Spam.bar.ncalls ->  Spam是一个类 Spam.__dict__['bar']  'bar'实例有get方法。None  Spam  instance=None cls=Spam 所以直接返回self 即Spam.bar这个Profiled实例。实例有ncall属性。我草这嵌套  6666666666
'''
print(Spam.__dict__)  #有个'bar'实例
#types.MethodType(obj) 把方法绑定实例上 可以百度这个关键词

'''

import types
def fn_get_grade(self):
    if self.score >= 80:
        return 'A'
    if self.score >= 60:
        return 'B'
    return 'C'
 
class Person(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
  下面我们将fn_get_grade()方法添加到实例上：

>>> p1 = Person('Bob', 90)
>>> p1.get_grade = types.MethodType(fn_get_grade, p1, Person)
>>> print p1.get_grade()
A
>>> p2 = Person('Alice', 65)

class MethodType:
    __func__ = ...  # type: _StaticFunctionType
    __self__ = ...  # type: object
    __name__ = ...  # type: str
    __qualname__ = ...  # type: str
    def __init__(self, func: Callable, obj: object) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> Any: ...
    

显然只有当实例被使用的时候绑定方法才会被创建 即：s.bar.ncalls  -》 type(b).__dict__['x'].__get__(b,type(b)) Spam.__dict__['bar'] 是一个Profiled obj
然后__get__(s,Spam)

return types.MethodType(s) 应该还是s的实例之类的。不管了。其余在用在百度。反正还是可以用ncalls。 没有这句。不能调用s.bar.ncalls！

'''
