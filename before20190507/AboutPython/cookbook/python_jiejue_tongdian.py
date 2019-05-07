# 专题解决痛点   __xx__各种方法 描述器 装饰器  以及高级操作：元类  内存视图memoryview  websocket asycnio协程  Autobahn库  SignalR库

# 也许是python难一点和精华一点的部分


# __xx__方法。  python学习手册第29章   运算符重载  31章 属性管理技术
# __getitem__ 索引，分片，迭代

'''
class Stepper:
    def __getitem__(self, item):
        return self.data[item]

x=Stepper()
x.data='Spam'
print(x[1],x[2:4])
for y in x:
    print(y,end='')

# next知道StopIteration为止
#用户自定义的迭代器

class Squares:
    def __init__(self,start,stop):
        self.__value=start-1
        self.__stop=stop

    def __iter__(self):
        return self

    def __next__(self):
        if self.__value == self.__stop:
            raise StopIteration
        self.__value += 1
        return self.__value ** 2
'''
'''
for i in Squares(1,5):
    print(i,end='')

x=Squares(1,6)
I=iter(x)
print(next(I))
'''

# __iter__对象会在调用过程中明确的保留状态信息，只循环换一次。用一次就少一次，用完就为空。但是生成器会保留。毕竟保存的是算法
# __getattr__  nice!
# __setattr__重写的时候通过__dict__属性来赋值  跟__getattr__一样是属性拦截只不过是去属性字典中设置而不是获取 x.a是获取  x.a=y是设置

'''
class accesscontrol:
    def __setattr__(self,attr,value):
        if attr == 'age':
            self.__dict__[attr] = value
        else:
            raise AttributeError(attr + 'not allowed')

acc=accesscontrol()
acc.age=40
print(acc.age)  #40
# acc.name='mel'  AttributeError: namenot allowed

#__call__ nice! 除了init str外最常用的方法.保留状态信息

class prod:
    def __init__(self,value):
        self.__value=value
    def __call__(self,other):
        return self.__value * other

x=prod(3)
print(x(3))   #9
'''


#__slots__属性  只有__slots__列表内的变量名可赋值为实例属性。实例属性名必须在引用前赋值
# 单独定义了__slots__
# 列出所有实例属性的代码

'''
class D:
    __slots__ = ['a','b']
    # def __init__(self): self.d=4  报错 AttributeError: D object has no attribute 'd'


class D:
    __slots__ = ['a','b','__dict__']
    c=3
    def __init__(self): self.d=4

x=D()


print(x.d)
print(x.__dict__)
print(x.__slots__)
# print(x.a)  AttributeError: a 要先赋值
x.a=1
print(getattr(x,'a'))  # 1

x.b=2

for attr in list(getattr(x,'__dict__',[])) + getattr(x,'__slots__',[]):  #我草还可以这样写
    print(attr,'=>',getattr(x,attr))

描述符的时候还要讲的。总之__slots__就是跟__dict__相关的
'''

# propertiy是跟getattr和setattr相关的。具体优缺点后面探究

'''
class newprops(object):
    def getage(self):
        return 40  # 相当于 def getage(self): return _age  只不过_age=40 参照propertiy的初始化
    def setage(self,value):
        print('set age:',value)
        self._age=value

    age=property(getage,setage,None,None)

x=newprops()
# print(x.hehe)  报错没有hehe
print(x.age)  #
x.age=42
print(x._age)  #把age的值给_age
x.job='trainer'
print(x.job)  #真不太清楚为啥 job这里没有调用getage  又遇到一个python学习手册P1098
print(list(getattr(x,'__dict__')))   ！！！！！！！！！！！！！！！！！！！  #['_age', 'job'] 真神奇 propertiy为啥可以直接加方法呢.肯定跟property类的其他方法有关。

'''
'''
def __init__(self, fget=None, fset=None, fdel=None, doc=None):  # known special case of property.__init__
    """
    property(fget=None, fset=None, fdel=None, doc=None) -> property attribute

    fget is a function to be used for getting an attribute value, and likewise
    fset is a function for setting, and fdel a function for del'ing, an
    attribute.  Typical use is to define a managed attribute x:

    class C(object):
        def getx(self): return self._x
        def setx(self, value): self._x = value
        def delx(self): del self._x
        x = property(getx, setx, delx, "I'm the 'x' property.")
'''

# 正常的实现如下
'''
class classic:
    def __getattr__(self, item):
        if item == 'age':
            return 40
        else:
            raise AttributeError

    def __setattr__(self, key, value):
        print('set:',key,value)

        if key == 'age':
            self.__dict__['_age'] = value
        else:
            self.__dict__[key]=value


x=classic()
print(x.age)
x.age=41
print(x._age)
x.job='trainer'
print(x.job)
'''

# 书中到此为止(python学习手册p828)并没有解释property可以直接加属性。和__slots__与__dict__方法的区别。
# getattr setattr内置方法和__getattr__ __setattr__总算搞清楚了  __getitem__ __setitem__搞清楚了。 __iter__ __next__搞清楚了。这两个是关联调用的只要调用了__iter__ 那么for或者next方法就要会调用__next__
 # __get__ __getagtribute__还没搞清楚

'''
 #  staticmethods classmethods  静态方法和类方法
def printNumInstances():
    print('created:', Spam.numInstance)

class Spam:
    numInstance=0
    def __init__(self):
        Spam.numInstance=Spam.numInstance + 1



a=Spam()
b=Spam()
c=Spam()

print(printNumInstances())  # created:3 None 果然是静态的。类的方法真是的
print(a.numInstance) #3 b c都是一样的。
'''

'''
class Methods():
    def imeth(self,x):
        print(self,x)

    def smeth(x):
        print(x)

    def cmeth(cls,x):
        print(cls,x)
'''

#突然有了self就是指this指针指的这个实例。staticmethod就是静态方法。cls就是类方法

# smeth=staticmethod(smeth)  #声明这是静态方法
# cmeth=classmethod(cmeth)
# print(Methods.smeth(3))   #3  None
# 不能调用没关系 懂意思就好
# Methods.smeth(3) 3  obj.smeth(4) 4
# Methods.cmeth(6) <class '__main__.Methods'> 5  等价于cmeth(Methods,5)

'''
class Spam:
    numInstance=0
    def __init__(self):
        Spam.numInstance=Spam.numInstance + 1

    def printNumInstances():
        print('Num of instances:',Spam.numInstance)


class Sub(Spam):
    def printNumInstances():
        print("extra stuff....")
        Spam.printNumInstances()

    printNumInstances=staticmethod(printNumInstances)

a=Sub()
b=Sub()
print(a.printNumInstances())
'''
'''
extra stuff....
Num of instances: 2
None

print(Sub.printNumInstances())

extra stuff....
Num of instances: 2
None


print(Spam.printNumInstances())


Num of instances: 2
None
'''

'''
class Spam:
    numInstances=0

    def count(cls):
        cls.numInstances += 1

    def __init__(self):
        self.count()

    count = classmethod(count)

class Sub(Spam):
    numInstances = 0  # 这两个numInstance真让人迷糊。算了。很杂技不去写这么让人误解的代码。搓比
    def __init__(self):
        Spam.__init__(self)  #有点不太明白这里的操作self指的是谁呢

class Other(Spam):
    numInstances = 0

x=Spam()
y1,y2=Sub(),Sub()
z1,z2,z3=Other(),Other(),Other()
print(x.numInstances,y1.numInstances,z1.numInstances)
print(Spam.numInstances,Sub.numInstances,Other.numInstances)
# (1,2,3)并不随Sub和Other的增多而增多
'''

# python学习手册 到此为止P850剩5个问题
# __slots__和__dict__
# __get__ __getattribute__
# 解答：getattr是内置方法。调用点号。 __getattr__是拦截未定义的属性 __getattribute__是拦截所有的属性必须小心避免通过把属
# 性访问传递给超类而导致递归循环。#通过使用同样的技术：命名空间字典或者超类方法调用。  简单来说 __getattrbute__别用少用。用了也要采用超类方法调用

# property可以添加方法  这个方法默认到了dict中。 解答：现在property和描述符高清了。其实就是重写__get__ __set__ __del__  添加一个貌似可以用点号操作看起来的是属性，只不过点号就是用重写的get 赋值就是用重写set而已。
#property()函数中的三个函数分别对应的是获取属性的方法、设置属性的方法以及删除属性的方法，这样一来，外部的对象就可以通过访问x的方式，来达到获取、设置或删除属性的目的。

# 子类的__init__(self) 然后super__init__(self) 这里的self到底指的是啥 #解答：在哪个类中就是哪个类的实例  python学习手册 P1031 当一个方法名绑定只是绑定到一个简单的函
# 数，Python向s e l f传递了隐含的主体实例；当它是一个可调用类的实例的时候，就传递这个类的实例。

'''
class PropSquare:
    def __init__(self,start):
        self.value=start

    def getX(self):
        return self.value ** 2
    def setX(self,value):
        self.value=value
    X=property(getX,setX)  #添加了X属性

p=PropSquare(3)
print(p.X)
p.X=4
print(p.X)
'''

#装饰器
'''
@decorator
def func(args):...

等价于 
def func(args):...
func=decorator(func)

class Person:
@property
def name(self): ...

传给property的第一个参数fget
class Person:
def name(self): ...
name = property(name)  #属性，函数 name不同
'''




'''
__getattr__和__setattr__方法，把未定义的属性获取和所有的属性赋值指向通用
的处理器方法。
__getattribute__方法，把所有属性获取都指向Python 2.6的新式类和Python 3.0的
所有类中的一个泛型处理器方法。·
p r o p e r t y内置函数，把特定属性访问定位到get和set处理器函数，也叫做特性
（Property）。
描述符协议，把特定属性访问定位到具有任意get和set处理器方法的类的实例。
'''

'''
object.__get__(self, instance, owner) 
如果class定义了它，则这个class就可以称为descriptor。owner是所有者的类，instance是访问descriptor的实例，如果不是通过实例访问，而是通过类访问的话，instance则为None
'''

'''
class Descriptor(object):
    def __get__(self, instance, owner):
        print(self,instance,owner,sep='\n')

class Subject:
    attr=Descriptor()

x=Subject()
x.attr
'''
'''
<__main__.Descriptor object at 0x10e9f6f98>
<__main__.Subject object at 0x10e9f6f28>
<class '__main__.Subject'>


Subject.attr

<__main__.Descriptor object at 0x105efbf98>
None
<class '__main__.Subject'>



self 就是Descriptor的实例
X.attr -> Descriptor.__get__(Subject.attr, X, Subject)

'''

# 类中包含另外一个类实例。然后另一个类定义了__get__
'''
class Descriptor:
"docstring goes here"
def __get__(self, instance, owner): ... # Return attr value
def __set__(self, instance, value): ... # Return nothing (None)
def __delete__(self, instance): ... # Return nothing (None)
'''

#特性和描述符有很强的相关性——p r o p e r t y内置函数只是创建描述符的一种方便方式

'''
class Property:
    def __init__(self,fget=None,fset=None,fdel=None,doc=None):
        self.fget=fget
        self.fset=fset
        self.fdel=fdel
        self.__doc__=doc

    def __get__(self,instance,instancetype=None):
        if instance is None:
            return self
        if self.fget is None:
            raise AttributeError("can't get attribute")
        return self.fget(instance)

    def __set__(self,instance,value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(instance,value)

    def __delete(self,instance):
        if self.fdel is None:
            raise AttributeError("can't set attribute")
        self.fdel(instance)

class Person:
    def getName(self): ...
    def setName(self): ...
    name = Property(getName,setName)

'''
'''
这个Property类捕获了带有描述符协议的属性访问，并且把请求定位到创建类的时候在
描述符状态中传入和保存的函数或方法。例如，属性获取从Person类指向Property类的
__get__方法，再回到Person类的getName
'''


# 于__getattribute__和__setattr__针对所有的属性运行，因此，它们的代
# 码要注意在访问其他属性的时候避免再次调用自己并触发一次递归循环
#python 学习手册P989  避免循环：通过使用同样的技术：命名空间字典或者超类方法调用。


#python学习手册 p994 property 描述符  __getattr__ __getattribute__

#装饰器  函数装饰器 类装饰器

'''
@decorator
def F(arg): ... 
F(99)

def F(arg): ...
F=decorator(F)
F(99)

func(6,7) 《=》decorator(func)(6,7)   #这个是重点

'''

'''
def decorator(F):
    def wrapper(*args):
        # Use F and args
        # F(*args) calls original function
        # test 一下
        F(*args)
        print('hehe ok')
    return wrapper  # fun(6,7）的结果是42 hehe ok
    # return F   fun(6,7)的结果是42

@decorator
def fun(x,y): print(x*y)
fun(6,7)  #hehe ok
'''

'''
class decorator:
    def __init__(self,func):
        self.x_func=func
    def __call__(self,*args):
        # use self.x_func and args
        # self.x_func(*args) calls original function
        self.x_func(*args)
        print('hehe ok')  

@decorator
def func(x,y): print(x * y)
func(6,7)   # 42 hehe ok
'''


# 支持方法装饰
'''
def decorator(F):
    def wrapper(*args): ...
        #   F(*args) runs func or method
    return wrapper

@decorator
def func(x,y): ...

func(6,67)

class C:
    @decorator
    def method(self,x,y):
        ...
x=C()
x.method(6,7)  #wrapper(x,6,7)
'''



# 类装饰器
'''
@decorator
class C: ...
x=C(99)

class C: ...
C=decorator(C)
x=C(99)

 x=C(99) <==> decortor(C)(99)


'''

'''
def decorator(cls):
    class Wrapper:
        def __init__(self,*args):
            self.wrapped=cls(*args)
        def  __getattr__(self, item):
            return getattr(self.wrapped,item)

    return Wrapper

@decorator
class C:
    def __init__(self,x,y):
        self.attr='spam'

x = C(6,7)
print(x.attr) #spam
# 类中有类，有必要吗。
'''

# 支持多个实例
'''
def decorator(C):
    class Wrapper:
        def __init__(self,*args):
            self.wrapped=C(*args)
    return Wrapper


class Wrapper:...
def decorator(C):
    def onCall(*args):
        return Wrapper(C(*args))
    return onCall
'''



# 装饰器嵌套
'''
@A
@B
@C

def f(...): ...

等价于
def f(...):...
f=A(B(C(f)))

f(args) <=> A(B(C(f)))(args)

多个类装饰器
@spam
@eggs
class C: ...
x=C()

class C: ...
C=spam(eggs(C))
x=C()

x=C() <=>  spam(eggs(C))()

'''

# 函数装饰器 return a callable: nested def, class with __call__, etc.
# 装饰器参数  函数装饰器和类装饰器都接收参数
'''
@decorator(A,B)
def F(arg): ...
F(99) <=> decorator(A,B)(F)(arg)

'''

'''
def decorate(O):
# Save or augment function or class O
return O
@decorator
def F(): ... # F = decorator(F)
@decorator
class C: ... # C = decorator(C)
'''
#返回最初装饰的对象而不是返回一个包装器，就可以管理函数和类自身而不是管理随后对它们的调用
# 跟踪调用  计算调用

'''
#计数器！！！！！！！
class tracer:
    lei_count=1

    def __init__(self,func):
        self.lei_count += 1
        self.calls=0
        self.func=func
    def __call__(self, *args):

        self.calls += 1
        print(self.calls,self.lei_count)

@tracer
def spam(): print()

@tracer
def hehe(): print('hehe')

spam()  #1 2
spam()  #2 2
hehe()  #1 2
#我的猜测是不同函数导致了类的实例不同。就算spam参数不同但是tracer实例相同。类属性一直就是2
#类属性实例属性是两个不同的概念
'''

#状态信息保存

# 使用嵌套函数来装饰方法
'''
def decorator(F):
    def wrapper(*args): ...
        #   F(*args) runs func or method
    return wrapper

@decorator
def func(x,y): ...

func(6,67)

class C:
    @decorator
    def method(self,x,y):
        ...
x=C()
x.method(6,7)  #wrapper(x,6,7)
'''
# 使用描述符装饰方法  装饰器又是描述符  装饰器可以是函数也可能是类。类就__call__方法。函数就返回一个函数


'''
# python 学习手册p1033 我草这个有点复杂。先跳过
class tracer(object):
    def __init__(self,func):
        self.calls=0
        self.func=func
    def __call__(self, *args, **kwargs):
        self.calls +=  1
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args,**kwargs)
    def __get__(self, instance, owner):
        return wrapper(self,instance) #这里的self对应wrapper的desc

class wrapper:
    def __init__(self,desc,subj):
        self.desc=desc
        self.subj=subj
    def __call__(self, *args, **kwargs):
        return self.desc(self.subj,*args,**kwargs)

@tracer
def spam(a,b,c): ...


class Person:
    @tracer
    def giveRaise(self,percent): ...  #因为trace是个描述类。 tracer又装饰。 所以这里就相当于有个tracer的实例在Person中

听说是等价于。虽然好理解意思。但是这个函数中定义函数实在有点别扭

class tracer(object):
    def __init__(self,func):
        self.calls=0
        self.func=func
    def __call__(self, *args, **kwargs):
        self.calls +=  1
        print('call %s to %s' % (self.calls, self.func.__name__))
        return self.func(*args,**kwargs)
    def __get__(self, instance, owner):
        def wrapper(*args,**kwargs):
            return self(instance,*args,**kwargs)
        return wrapper  

# 其实就是函数做装饰器修饰函数和放到类中。类也可以做装饰器放到函数和类的函数中
'''

# 计时

'''
import time

class timer:
    def __init__(self,func):
        self.func=func
        self.alltime=0

    def __call__(self,*args,**kwargs):
        start=time.clock()
        result=self.func(*args,**kwargs)
        elapsed=time.clock()-start
        self.alltime += elapsed
        print('%s: %.5f, %.5f' % (self.func.__name__, elapsed, self.alltime))
        return result

@timer
def listcomp(N):
    return [ x*2 for x in range(N)]

@timer
def mapcall(N):
    return map((lambda x: x*2),range(N))


result=listcomp(5)
listcomp(50000)
listcomp(500000)
listcomp(1000000)
print(result)
print('allTime = %s' % listcomp.alltime)

print('')
result = mapcall(5)
mapcall(50000)
mapcall(500000)
mapcall(1000000)
print(result)
print('allTime = %s' % mapcall.alltime)
print('map/comp = %s' % round(mapcall.alltime / listcomp.alltime, 3))
'''
'''
listcomp: 0.00001, 0.00001
listcomp: 0.00639, 0.00640
listcomp: 0.03945, 0.04585
listcomp: 0.09093, 0.13678
[0, 2, 4, 6, 8]
allTime = 0.136785

mapcall: 0.00001, 0.00001
mapcall: 0.00000, 0.00001
mapcall: 0.00000, 0.00002
mapcall: 0.00000, 0.00002
<map object at 0x106811208>
allTime = 1.7000000000017e-05
map/comp = 0.0
'''



#添加装饰器参数
'''
def timer(label=''):
    def decorator(func):
        def onCall(*args):
            print(label,...)
        return onCall
    return decorator
@timer('==>')
def listcomp(N):
    return [ x*2 for x in range(N)]

listcomp(3)
'''

# 装饰器把类放到函数中。def 一个函数就相当于产生了一个实例。实例形成就会调用call方法。我草66  python学习手册1038
# 虽然把类放到函数中，而且类中还有函数 。有点是否不注意可读性？



#编写类装饰器  单体类 跟踪对象接口
'''
instance={}
def getInstance(aclass,*args):
    if aclass not in instance:  #保证了单例
        instance[aclass] = aclass(*args)
        return instance[aclass]  
    
def singleton(aclass):
    def oncall(*args):
        return getInstance(aclass,*args)
    return oncall   # 又是这种函数中返回函数的操作 都是跟装饰器相关的



@singleton
class Person:
    def __init__(self,name,hours,rate):
        self.name=name
        self.hours=hours
        self.rate=rate
    def pay(self):
        return self.hours*self.rate

@singleton
class Spam:
    def __init__(self,val):
        self.attr=val

bob=Person('bob',40,10)
sue=Person('sue',30,20)
print(bob.name,bob.pay())
print(sue.name,sue.pay())
x=Spam(43)
y=Spam(45)
print(x.attr,y.attr)

或者:
'''
'''
class singleton:
    def __init__(self,aclass):
        self.aclass=aclass
        self.instance=None
    def __call__(self, *args):
        if self.instance == None:
            self.instance=self.aclass(*args)
        return self.instance
'''

# 装饰器到此为止吧。各种各样的装饰器太多了。看不完的。

# 终于要到最后的元类  协程ayscnio websocket库三大件了。

# P1089 class语句协议


'''
class Meta(type):
    def __new__(meta,classname,supers,classdict):
        print(classname,supers,classdict)
        return type.__new__(meta,classname,supers,classdict)
    def __init__(Class,classname,supers,classdict):
        print(classname,supers,classdict)
        print(list(Class.__dict__.keys()))

class Eggs:...

class Spam(Eggs,metaclass=Meta): data=1
x=Spam()
print(x.data)

Spam (<class '__main__.Eggs'>,) {'__module__': '__main__', '__qualname__': 'Spam', 'data': 1}
Spam (<class '__main__.Eggs'>,) {'__module__': '__main__', '__qualname__': 'Spam', 'data': 1}
['__module__', 'data', '__doc__']
1
'''

## __call__ can be redefined, metas can have metas  python学习手册P1094

'''
class Client1:
    def __init__(self, value):
        self.value = value

    def spam(self):
        return self.value * 2

class Client2:
    value = 'ni?'

def eggsfunc(obj):
    return obj.value * 4

def hamfunc(obj, value):
    return value + 'ham'

Client1.eggs = eggsfunc
Client1.ham = hamfunc
Client2.eggs = eggsfunc
Client2.ham = hamfunc
X = Client1('Ni!')
print(X.spam())
print(X.eggs())
print(X.ham('bacon'))
Y = Client2()
print(Y.eggs())
print(Y.ham('bacon'))
'''

'''
def eggsfunc(obj):
    return obj.value * 4

def hamfunc(obj,value):
    return value+'ham'

class Exrtender(type):
    def __new__(meta,classname,supers,classdict):
        classdict['eggs']=eggsfunc
        classdict['ham'] = hamfunc
        print(classname,supers,classdict)
        return type.__new__(meta,classname,supers,classdict)

class Client1(metaclass=Exrtender):
    def __init__(self,value):
        self.value=value

class Clinet2(metaclass=Exrtender):
    value='ni?'

x=Client1('ni!')
y=Clinet2()
'''

# 类装饰器可以管理类和实例。 元类也一样
# p1102 元类可以是函数？ 应该可以 靠的是return 上面Exrtender是返回一个新的类





'''
def Tracer(classname,supers,classdict):
    aClass=type(classname,supers,classdict)
    class Wrapper:
        def __init__(self,*args,**kwargs):
            self.wrapped=aClass(*args,**kwargs)
        def __getattr__(self, item):
            print("Trace",item)
            return getattr(self.wrapped,item)
    return Wrapper

class Person(metaclass=Tracer):
    def __init__(self,name,hours,rate):
        self.name=name
        self.hours=hours
        self.rate=rate
    def pay(self):
        return self.hours*self.rate


bob=Person('bob',40,50)
print(bob.name)
print(bob.pay())
print(bob.__class__.__name__)


Trace name
bob
Trace pay
2000
Wrapper
'''

'''
# 对方法应用装饰器
#纯装饰器

# 这种函数返回函数，又继续返回函数操作的真只能装饰器元类之类的操作了
def tracer(func):
    calls=0
    def onCall(*args,**kwargs):
        nonlocal calls
        calls += 1
        print('call %s to %s' % (calls, func.__name__))
        return func(*args,**kwargs)
    return onCall

import time
#装饰器和元类结合
'''
'''
class MetaTrace(type):
    def __new__(meta,classname,supers,classdict):
        for attr,attrval in classdict.items():
            classdict[attr]=tracer(attrval)
        return type.__new__(meta,classname,supers,classdict)  #TypeError: type __qualname__ must be a str, not function

class Person(metaclass=MetaTrace):
    def __init__(self,name,pay):
        self.name=name
        self.pay=pay
    def giveRaise(self,percent):
        self.pay *= (1.0+percent)

    def lastName(self):
        return self.name.split()[-1]

bob = Person('Bob Smith', 50000)
sue = Person('Sue Jones', 100000)
print(bob.name, sue.name)
sue.giveRaise(.10)
print(sue.pay)
print(bob.lastName(), sue.lastName())

程序跑不起来。但是装饰器和元类结合还是很好用的，虽然在p1105看不懂为啥call是怎么变化的

'''''
# p1106把任何装饰器应用于方法
#ok暂时告一段落。  装饰器可以是函数或者类。元类也可以是函数或者类然后就看返回值，类可以更通用写
# 描述符只不过是一个类中有另外一个类的实例。而且另外一个类定义了__get__ __set__等方法


#值得回味的页数
# P979 986Property和Person中的self是Property的实例也就是Person.name
# 989 避免属性拦截方法中的循环
#p1015函数装饰器 装饰器是个函数也返回一个函数  p1018函数装饰器支持方法装饰  p1019类装饰器用法实现 装饰器可能是个函数也可能是个类，返回可能是个函数也可能是个类。装饰的是个函数也可能是个类
# p1027类装饰器装饰函数我醉了。 类装饰器装饰函数主要是__call__把。 p1033描述器与装饰器结合  #p1040这个单体类例子
#小心P1045  保持多个实例的错误  #p1056 accessControl这个函数 类  函数的嵌套。心累 装饰器看不完的。类和函数各种嵌套修饰的也可能是函数和类。真蛋疼
#p1081的简介  #p1086 元类是类，是type的子类，用来生成别的类。类本来就是由type函数调用call方法。然后new和init形成的 可以交给元类去干这事
#p1089-1091全部  p1092MetaOne  1092工厂函数  1094元类重载类创建调用   总之就是用new形成类或者直接返回类  1095常规重载类创建调用
#p1096 实例和继承的关系  1099往类中添加方法  1101 1102

# memoryview 搜索就ok。 内置函数也就那么多个

# 协程asycnio和websocket
#协程初步理解。
'''

event_loop 事件循环：中心执行器，执行多个task

coroutine 协程：协程对象，指一个使用async关键字定义的函数，它的调用不会立即执行函数，而是会返回一个协程对象。协程对象需要注册到事件循环，由事件循环调用。

task 任务：一个协程对象就是一个原生可以挂起的函数，任务则是对协程进一步封装，其中包含了任务的各种状态 Pending Running Done  Cacelled。就是多个coroutine

future: 代表将来执行或没有执行的任务的结果。它和task上没有本质上的区别

async/await 关键字：python3.5用于定义协程的关键字，async定义一个协程，await用于挂起阻塞的异步调用接口。协程之间的转换。看书签中那个图所有都明白了

https://www.oschina.net/translate/asynchronous-programming-in-python-asyncio
http://python.jobbole.com/87541/
https://segmentfault.com/a/1190000012631063
'''

'''
import asyncio
import time
from datetime import datetime

async def custom_sleep():
    print('SLEEP',datetime.now())
    await asyncio.sleep(1)  # 比time.sleep(1)快2s。 await会切换任务。为啥是以耗时多的为准呢。

async def factorial(name,number):
    f=1
    for i in range(2,number+1):
        print('Task {}:Comppute factorial({})'.format(name,i))
        await  custom_sleep()
        f *= i
    print('Task {}:Comppute factorial({}) is {},now time is {}\n'.format(name,number,f,datetime.now()))

start=time.time()
loop=asyncio.get_event_loop()
task=[asyncio.ensure_future(factorial('A',4)),asyncio.ensure_future(factorial('B',3))]  #切换到任务之后就必须执行了io操作了。B在sleep的时候A也在sleep吗
loop.run_until_complete(asyncio.wait(task))
loop.close()
end=time.time()
print('Total time:{}'.format(end-start))
'''


'''
import asyncio
import time
from datetime import datetime

async def A_custom_sleep():
    print('A SLEEP',datetime.now())
    await asyncio.sleep(1)  # 比time.sleep(1)快2s。 await会切换任务。为啥是以耗时多的为准呢。

async def B_custom_sleep():
    print('B SLEEP',datetime.now())
    await asyncio.sleep(2)

async def A_factorial(name,number):
    f=1
    for i in range(2,number+1):
        print('A Task {}:Comppute factorial({})'.format(name,i))
        await  A_custom_sleep()
        f *= i
    print('A Task {}:Comppute factorial({}) is {},now time {}\n'.format(name,number,f,datetime.now()))

async def B_factorial(name,number):
    f=1
    for i in range(2,number+1):
        print('B Task {}:Comppute factorial({})'.format(name,i))
        await  B_custom_sleep()
        f *= i
    print('B Task {}:Comppute factorial({}) is {},now time {}\n'.format(name,number,f,datetime.now()))

start=time.time()
loop=asyncio.get_event_loop()
task=[asyncio.ensure_future(A_factorial('A',3)),asyncio.ensure_future(B_factorial('B',4))]  #有意思，改改AB的顺序，改改number，改改各自sleep的时间
loop.run_until_complete(asyncio.wait(task))
loop.close()
end=time.time()
print('Total time:{}'.format(end-start))

# 明白了。io或者sleep不管是哪个任务。程序还是继续执行的。只不过cpu会处理其他任务而已。这里不管是睡2s还是1s，也不管是哪个任务。都是会程序睡，cpu处理其他任务的。全部在睡那么cpu也空闲了。有一个睡醒了cpu也就跟着继续执行了


A Task A:Comppute factorial(2)
A SLEEP 2018-08-07 19:30:48.600935  #A开始睡了
B Task B:Comppute factorial(2)
B SLEEP 2018-08-07 19:30:48.600981  #B开始睡了
A Task A:Comppute factorial(3)      #A睡醒了
A SLEEP 2018-08-07 19:30:49.605913  #A又开始睡了   ---这里和下面差了一秒
B Task B:Comppute factorial(3)      #B睡醒了
B SLEEP 2018-08-07 19:30:50.605955  #B又开始睡了
A Task A:Comppute factorial(3) is 6,now time 2018-08-07 19:30:50.606127   #A彻底睡醒了 跟上面的B刚开始睡时间相同

B Task B:Comppute factorial(4)     #B睡醒了
B SLEEP 2018-08-07 19:30:52.607662  #B又开始睡了
B Task B:Comppute factorial(4) is 24,now time 2018-08-07 19:30:54.612418  #B彻底醒了

Total time:6.01265287399292
'''


'''
Future是用来接受异步的结果的。是一个类
Task是将future和协程对象组合到一起，用于事件循环的。


 协程异步结果sleep ok —Future是用来接受异步的结果的。  future is done -future add done callback  ——task done  - 
asyncio.create_task(coro)
Wrap a coroutine coro into a task and schedule its execution. Return the task object.
The task is executed in get_running_loop() context, RuntimeError is raised if there is no running loop in current thread.
New in version 3.7.
class asyncio.Task(coro, *, loop=None)
A unit for concurrent running of coroutines, subclass of Future.
A task is responsible for executing a coroutine object in an event loop. If the wrapped coroutine yields from a future, the task suspends the execution of the wrapped coroutine and waits for the completion of the future. When the future is done, the execution of the wrapped coroutine restarts with the result or the exception of the future.
Event loops use cooperative scheduling: an event loop only runs one task at a time. Other tasks may run in parallel if other event loops are running in different threads. While a task waits for the completion of a future, the event loop executes a new task.



Await让出cpu控制权，就是切换到了另一个协程。遇到io则切换到另一个任务。io或者sleep继续执行。最后返回到第一个任务task

asyncio.ensure_future(coro_or_future, *, loop=None)
Schedule the execution of a coroutine object: wrap it in a future. Return a Task object.

If the argument is a Future, it is returned directly.

Note:create_task() (added in Python 3.7) is the preferable way for spawning new tasks.

the protocol parses incoming data and asks for the writing of outgoing data, while the transport is responsible for the actual I/O and buffering.

the protocol parses incoming data and asks for the writing of outgoing data, while the transport is responsible for the actual I/O and buffering.

When subclassing a protocol class, it is recommended you override certain methods. Those methods are callbacks: they will be called by the transport on certain events (for example when some data is received); you shouldn’t call them yourself, unless you are implementing a transport.

'''

'''
import asyncio

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self,message,loop):
        self.message=message
        self.loop=loop

    def connection_made(self,transport):   #代表这个传输。这个connection_made是自动调用的
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('the server closed the connection')
        print('stop the event loop')
        self.loop.stop()





loop=asyncio.get_event_loop()
messag='hello world'
coro=loop.create_connection(lambda: EchoClientProtocol(messag,loop),'127.0.0.1',8888)
print(type(coro),coro)   #<class 'generator'> <generator object BaseEventLoop.create_connection at 0x106bc9728>
loop.run_until_complete(coro)   #这里的task和future是啥呢
loop.close()
'''



'''
import asyncio
from socket import socketpair

# Create a pair of connected sockets
rsock, wsock = socketpair()
loop = asyncio.get_event_loop()

class MyProtocol(asyncio.Protocol):
    transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print("Received:", data.decode())

        # We are done: close the transport (it will call connection_lost())
        self.transport.close()

    def connection_lost(self, exc):
        # The socket has been closed, stop the event loop
        loop.stop()

# Register the socket to wait for data
connect_coro = loop.create_connection(MyProtocol, sock=rsock)
transport, protocol = loop.run_until_complete(connect_coro)
print(type(transport),type(protocol),transport,protocol,type(protocol.transport),protocol.transport)
if(transport == protocol.transport):
    print('oh my god')

# Simulate the reception of data from the network
loop.call_soon(wsock.send, 'abc'.encode())

# Run the event loop
loop.run_forever()

# We are done, close sockets and the event loop
rsock.close()
wsock.close()
loop.close()

#<class 'asyncio.selector_events._SelectorSocketTransport'> <class '__main__.MyProtocol'> <_SelectorSocketTransport fd=3 read=polling write=<idle, bufsize=0>> <__main__.MyProtocol object at 0x10f96ea20> <class 'asyncio.selector_events._SelectorSocketTransport'> <_SelectorSocketTransport fd=3 read=polling write=<idle, bufsize=0>>
# oh my god
#Received: abc


future = asyncio.run_coroutine_threadsafe(coro_func(), loop)
result = future.result(timeout)  # Wait for the result with a timeout

websocket协议是itef的  http://tools.ietf.org/html/draft-hixie-thewebsocketprotocol-76  可以搜索相关websocket的消息
websocket的关键是 opcode  websocket-client有个recv_data_frame 一直读消息。如果是opcode是close就close调用on_close方法。如果是ping或者pong就ping或者pong方法
可以用socks或者http做代理握手。只不过添加了一些websocket的字段，服务端会添加base64然后掩码之类的  就可以传输了。
asyncio的transport和protocol也可以有相同的作用。但是源码看不见还是少用把。就用它的协程功能就好了。Autobahn就是使用asyncio的transport和protocol来完成websocket的。
难以维护，pass。

websocket-client源码大概看了下。根本不需要在on_close去写重连这就是个思维坑。回调函数是自己控制的。close了函数就执行完了。

'''



'''
# await 与awaitable对象  __await__方法。 生成器，yield，send，协程的端倪从以下例子可以搞出来
import asyncio

class B:
    def __iter__(self):
        print('1')
        return self
    def __next__(self):
        print('2')
        raise StopIteration('end')


class A:
    def __await__(self):
        print('0')
        return B()

async def a():
    s = await A()
    print(s)



loop = asyncio.get_event_loop()
loop.run_until_complete(a())
loop.close()
'''


















