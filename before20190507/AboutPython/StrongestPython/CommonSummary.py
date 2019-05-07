 # * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2019/1/28 2:31 PM
#  Author           purplecity
#  Name             zongjie.py
#  Description
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 普通参数可以用关键字参数传递。关键字参数除了用a=b这种形式传递参数外,也可以用普通参数传递  关键字参数还能用字典传递 关键字参数可以当做变量使用    关键字参数跟默认参数一样的意思  普通参数跟位置参数一样的意思  命名关键字参数用*分隔 可变参数就是*args **kwargs

# 该想到经常能用的模块: inspect检查对象相关eg:p291  operator操作对象相关 functools函数对象相关。itertools跟迭代相关。还有built-in func 就是想找啥方法是优先从这些库找
#buile-in:  https://docs.python.org/3/library/functions.html
#itertools:https://docs.python.org/3/library/itertools.html
#operator:https://docs.python.org/3/library/operator.html
#inspect:https://docs.python.org/3/library/inspect.html

assert expression 等价于
if not expression: raise AssertionError

# lambda就是创建匿名函数。 lambda 参数:表达式  返回函数对象。
'''
lambda parameters: expression
def <lambda>(parameters):
    return expression
'''

'''
#这一章到现在就是一个lambda和可调用对象的收获。
#不仅 Python 函数是真正的对象，任何 Python 对象都可以表现得像函
#数。为此，只需实现实例方法 __call__。


import random

class BingoCage:
    def __init__(self,items):
        self.__items  = list(items)
        random.shuffle(self.__items)

    def pick(self):
        try:
            return self.__items.pop()
        except IndexError:
            raise LookupError('pick from empty BingoCage')
    def __call__(self):
        return self.pick()

#bingo.pick() 的快捷方式是 bingo()。
'''

'''
classmethod和staticmethod
class A(object):
    def foo(self, x):
        print("executing foo(%s,%s)" % (self, x))
        print('self:', self)
    @classmethod
    def class_foo(cls, x):
        print("executing class_foo(%s,%s)" % (cls, x))
        print('cls:', cls)
    @staticmethod
    def static_foo(x):
        print("executing static_foo(%s)" % x)
a = A()

class B(A):
    ...


调用方式:
a.foo("putong")
A.foo(a,"putong")
B.foo(B(),"putong")

print("*"*10)

A.class_foo("test")
a.class_foo("test")#别扭
B.class_foo("test")

print("*"*10)

A.static_foo("test2")
a.static_foo("test2")
B.static_foo("test2")
# staticmethod一点用没有。完全没必要

'''

'''

# __new__ __init__ __dir__ __dict__ __slots__ __mro__/super  class/instance attrbute    direct assignment

1. class attrbute --> class and instance all can change
class Dog:
    kind = [] # class attrbute

    def __init__(self,x):
        self.y = x # instance attrbute


d=Dog("yes")
print(Dog.kind)
Dog.kind.append("letsee")
print(d.kind)
d.kind.append("letsee2")
print(Dog.kind)

2 dir() __dict__ direct assignment

object.__dict__
A dictionary or other mapping object used to store an object’s (writable) attributes.

dir(object)
If the object is a module object, the list contains the names of the module’s attributes.
If the object is a type or class object, the list contains the names of its attributes, and recursively of the attributes of its bases.


# instance or class can use *.x to get the attrbute;  because a.x will has a lookup chain starting with a.__dict__['x'], then type(a).__dict__['x'], and continuing through the base classes of type(a) excluding metaclasses.
#__get__优先级大于__getattr__: offcial:Called when the default attribute access fails with an AttributeError (either __getattribute__() raises an AttributeError because name is not an instance attribute or an attribute in the class tree for self; or __get__() of a name property raises AttributeError). This method should either return the (computed) attribute value or raise an AttributeError exception.
#Note that if the attribute is found through the normal mechanism, __getattr__() is not called. ----https://docs.python.org/3/reference/datamodel.html?highlight=_get_#object.__get__
# *.x=y will  assignment attribute x = value y at *.__dict__   __setattr__ 优先__set__, __delattr__优先__delete__.  不管是方法属性还是值属性都往*.__dict__中插入


__class__
　　对象所属类的引用（即 obj.__class__ 与 type(obj) 的作用相
同）。Python 的某些特殊方法，例如 __getattr__，只在对象的类中寻
找，而不在实例中寻找。


d=Dog("yes")

def transfer(instance,m): #只要是类属性第一个参数就是实例不管咋命名。
    if isinstance(instance,list):
        instance.y = m

Dog.transfer = transfer
Dog.transfer(d,"good")
#d.transfer(d,"good2") #TypeError: transfer() takes 2 positional arguments but 3 were given。实例调用类方法的时候是把自身当做参数调用类方法的
d.transfer("good2") # == Dog.transfer(d,"good2")
print(d.y)

dir 函数的目的
是交互式使用，因此没有提供完整的属性列表，只列出一组“重要的”属
性名。dir 函数能审查有或没有 __dict__ 属性的对象。dir 函数不会
列出 __dict__ 属性本身，但会列出其中的键。dir 函数也不会列出类
的几个特殊属性，例如 __mro__、__bases__ 和 __name__。如果没有
指定可选的 object 参数，dir 函数会列出当前作用域中的名称。


3 __slots__
Python 在各个实例中名为 __dict__ 的字典里存储实例属
性。为了使用底层的散列表提升访问速度，字典会消
耗大量内存。如果要处理数百万个属性不多的实例，通过 __slots__
类属性，能节省大量内存，方法是让解释器在元组中存储实例属性，而
不用字典。

继承自超类的 __slots__ 属性没有效果。Python 只会使用
各个类中定义的 __slots__ 属性。

定义 __slots__ 的方式是，创建一个类属性，使用 __slots__ 这个名
字，并把它的值设为一个字符串构成的可迭代对象，其中各个元素表示
各个实例属性。我喜欢使用元组，因为这样定义的 __slots__ 中所含
的信息不会变化

class Vector2d:
__slots__ = ('__x', '__y')
typecode = 'd'

在类中定义 __slots__ 属性的目的是告诉解释器：“这个类中的所有实
例属性都在这儿了！”这样，Python 会在各个实例中使用类似元组的结
构存储实例变量，从而避免使用消耗内存的 __dict__ 属性。如果有数
百万个实例同时活动，这样做能节省大量内存。

在类中定义 __slots__ 属性之后，实例不能再有
__slots__ 中所列名称之外的其他属性。这只是一个副作用，不是
__slots__ 存在的真正原因。不要使用 __slots__ 属性禁止类的
用户新增实例属性。__slots__ 是用于优化的，不是为了约束程序
员。
然而，“节省的内存也可能被再次吃掉”：如果把 '__dict__' 这个名称
添加到 __slots__ 中，实例会在元组中保存各个实例的属性，此外还
支持动态创建属性，这些属性存储在常规的 __dict__ 中。当然，把
'__dict__' 添加到 __slots__ 中可能完全违背了初衷，这取决于各个
实例的静态属性和动态属性的数量及其用法。粗心的优化甚至比提早优
化还糟糕。

4__new__ __init__

我们通常把 __init__ 称为构造方法，这是从其他语言借鉴过来的术
语。其实，用于构建实例的是特殊方法 __new__：这是个类方法（使用
特殊方式处理，因此不必使用 @classmethod 装饰器），必须返回一个
实例。返回的实例会作为第一个参数（即 self）传给 __init__ 方
法。因为调用 __init__ 方法时要传入实例，而且禁止返回任何值，所
以 __init__ 方法其实是“初始化方法”。真正的构造方法是 __new__。
我们几乎不需要自己编写 __new__ 方法，因为从 object 类继承的实现
已经足够了。
刚才说明的过程，即从 __new__ 方法到 __init__ 方法，是最常见
的，但不是唯一的。__new__ 方法也可以返回其他类的实例，此时，解
释器不会调用 __init__ 方法。

伪代码如下：
def object_maker(the_class, some_arg):
new_object = the_class.__new__(some_arg)
if isinstance(new_object, the_class):
the_class.__init__(new_object, some_arg)
return new_object
# 下述两个语句的作用基本等效
x = Foo('bar')
x = object_maker(Foo, 'bar')



'''
'''
5 __mro__ super

Return a proxy object that delegates method calls to a parent or sibling class of type.The search order is same as that used by __mro__ except that the type itself is skipped.
返回一个代理对象，该对象将方法调用 委托给 类型的父类或兄弟类。

        super() -> same as super(__class__, <first argument>)
        super(type) -> unbound super object
        super(type, obj) -> bound super object; requires isinstance(obj, type)
        super(type, type2) -> bound super object; requires issubclass(type2, type)


class C(B):
    def method(self, arg):
        super().method(arg)    # This does the same thing as:
                               # super(C, self).method(arg)

class.__mro__
This attribute is a tuple of classes that are considered when looking for base classes during method resolution.

class.mro()
This method can be overridden by a metaclass to customize the method resolution order for its instances. It is called at class instantiation, and its result is stored in __mro__.

class Root:
    def draw(self):
        # the delegation chain stops here
        assert not hasattr(super(), 'draw')

class Shape(Root):
    def __init__(self, shapename, **kwds):
        self.shapename = shapename
        super().__init__(**kwds)
    def draw(self):
        print('Drawing.  Setting shape to:', self.shapename)
        super().draw()

class ColoredShape(Shape):
    def __init__(self, color, **kwds):
        self.color = color
        super().__init__(**kwds)
    def draw(self):
        print('Drawing.  Setting color to:', self.color)
        super().draw()

class Moveable:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def draw(self):
        print('Drawing at position:', self.x, self.y)

class MoveableAdapter(Root):
    def __init__(self, x, y, **kwds):
        self.movable = Moveable(x, y)
        super().__init__(**kwds)
    def draw(self):
        self.movable.draw()
        super().draw()

class MovableColoredShape(ColoredShape, MoveableAdapter):
    pass

print(MovableColoredShape.__mro__)

MovableColoredShape(color='red', shapename='triangle',
                    x=10, y=20).draw()

'''


# with  else

'''
1 else:
for
　　仅当 for 循环运行完毕时（即 for 循环没有被 break 语句中止）
才运行 else 块。
while
　　仅当 while 循环因为条件为假值而退出时（即 while 循环没有被
break 语句中止）才运行 else 块。
try
　　仅当 try 块中没有异常抛出时才运行 else 块。官方文档
（https://docs.python.org/3/reference/compound_stmts.html）还指
出：“else 子句抛出的异常不会由前面的 except 子句处理。”
在所有情况下，如果异常或者 return、break 或 continue 语句导致
控制权跳到了复合语句的主块之外，else 子句也会被跳过。

2 with  PEP343

用来代替try/except/finally/


with EXPR as VAR:
    BLOCK
等价于
mgr = (EXPR)
exit = type(mgr).__exit__  # Not calling it yet
value = type(mgr).__enter__(mgr)
exc = True
try:
    try:
        VAR = value  # Only if "as VAR" is present
        BLOCK
    except:
        # The exceptional case is handled here
        exc = False
        if not exit(mgr, *sys.exc_info()):  #its type, value, and traceback are passed as arguments to __exit__(). Otherwise, three None arguments are supplied.
            raise
        # The exception is swallowed if exit() returns true
finally:
    # The normal and non-local-goto cases are handled here
    if exc:
        exit(mgr, None, None, None)


'''




# 引用 可变形
'''
每个变量都有标识、 类型和值。 对象一旦创建， 它的标识绝不会
变； 你可以把标识理解为对象在内存中的地址。 is 运算符比较两个
对象的标识； id() 函数返回对象标识的整数表示。
对象 ID 的真正意义在不同的实现中有所不同。 在 CPython 中， id() 返
回对象的内存地址， 但是在其他 Python 解释器中可能是别的值。 关键
是， ID 一定是唯一的数值标注， 而且在对象的生命周期中绝不会变


== 运算符比较两个对象的值（对象中保存的数据） ， 而 is 比较对象的
标识。

扁平：
str、 bytes 和 array.array 它们保存的不是引用， 而是在连续的内存中保存数据本身（字符、 字节和数字） 。
容器
有些对象里包含对其他对象的引用； 这些对象称为容器。如dict list set tuple

容器可变不可变指： 容器内的元素可变不可变。但是因为容器内的元素可能是引用。比如dict list set tuple
可变容器： 不可hash 包括  dict set list
不可变容器： tuple frozenset
但是因为容器内的元素可能是引用。比如dict list set tuple。所以不可变容器里面中引用元素所指的内存还是可以变的



浅拷贝：副本共享内部容器对象的引用
浅拷贝： 重新创建一块区域。如果元素是扁平或者值等就直接拷贝。如果是容器。拷贝的是容器的引用
深拷贝：不共享内部容器对象的引用

闯不创建副本：

+-*都会创建副本
简单的赋值不创建副本。
对 += 或 *= 所做的增量赋值来说， 如果左边的变量绑定的是不可变
对象(如元组tuple)， 会创建新对象； 如果是可变对象--list dict set， 会就地修改。所以列表的extend apend等都是就地修改


所有的创建副本都是浅拷贝。包括
1 list dict set等函数操作
2 切片。



l1 = [3, [66, 55, 44], (7, 8, 9)]
l2 = list(l1)
l1.append(100)
l1[1].remove(55)
print('l1:', l1)
print('l2:', l2)
l2[1] += [33, 22]
l2[2] += (10, 11)
print('l1:', l1)
print('l2:', l2)

l1: [3, [66, 44], (7, 8, 9), 100]
l2: [3, [66, 44], (7, 8, 9)]
l1: [3, [66, 44, 33, 22], (7, 8, 9), 100]
l2: [3, [66, 44, 33, 22], (7, 8, 9, 10, 11)]


浅拷贝的后果:
如果容器内部元素是不可变的。那么这样没有问题。还能节省内存。比如 a = [3, [66, 55, 44], (7, 8, 9)]  b = a.copy() a和b中的后两个元素都是引用指向相同的内存区域
但是，如果容器内部元素中有可变的元素，可能就会导致意想不到的问题。比如容器里面还有容器。那么拷贝后的对象对容器中的容器进行操作。可能就修改了原来的值
比如 a = [3, [66, 55, 44，[5,6]], (7, 8, 9)] b = a.copy  b[1][-1].append(7) 。 结果a也变了

函数传参传的是引用。即形参是是实参的别名。
所以给函数传参的时候如果是list千万要注意。第一要list()保存下副本 第二list中容器中的元素是不可变的。

我们可以实现特殊方法 __copy__() 和
__deepcopy__()，控制 copy 和 deepcopy 的行为


'''

# 描述符 特性


'''
描述符是最烂的设计。因为描述符是覆盖性描述符--就是变量命名相同导致的智障操作---干嘛命名相同呢？。不值的看。目前为止我觉得描述符就是python最失败的地方---智障设计
亏流畅的python还花了将近2章来描述。这里面也是错误连篇。枯涩难理解又一点都不实用跟python初衷完全背道而驰

特性:
（property），在不改变类接口的前提下，使用存取方法（即读值方法
和设值方法）修改数据属性。特性都是类属性，但是特性管理的其实是实例属性的存取。

特性协议允许我们把一个特定属性的get和set操作指向我们所提供的函数或方法(对特性attribute的存取.attribute .attribute=来调用fget fset方法来修改数据属性)
通过property内置函数来创建特性实例(其实就是一个property类实例)并将其分配给类属性

可以通过把一个内置函数的结果赋给一个类属性来创建一个特性：
attribute = property(fget, fset, fdel, doc)
这个内置函数的参数都不是必需的，并且如果没有传递参数的话，所有都取默认值
N o n e。这样的操作是不受支持的，并且尝试使用默认值将会引发一个异常。当使用它们
的时候，我们向fget传递一个函数来拦截属性访问，给fset传递一个函数进行赋值，并
且给f d e l传递一个函数进行属性删除；d o c参数接收该属性的一个文档字符串



class C:
    def __init__(self):
        self._x = None

    def getx(self):
        return self._x

    def sety(self, value):
        self._x = value

    def delz(self):
        del self._x

    x = property(getx, sety, delz, "I'm the 'x' property.")

@property其实就是把下面的函数当做fget传参返回特性实例。跟装饰器一样这个特性实例的名字就是fget那个函数。然后再.setter装饰一个fset函数。
class C:
    def __init__(self):
        self._x = None

    @property
    def x(self):
        """I'm the 'x' property."""
        return self._x

    @x.setter
    def y(self, value):
        self._x = value



    @x.deleter
    def z(self):
        del self._x
c=C()
c.y=4 #改变的是c._x
print(c._x)


'''



# 装饰器 闭包
'''
def make_average():

    #============================================
    series=[]  # free variables                 #
    def averager(new_value):                    #   闭
        series.append(new_value)                #
        total = sum(series)                     #   包
        return total/len(series)                #
    #=============================================
    return averager

#__code__	The code object representing the compiled function body.
#__closure__	None or a tuple of cells that contain bindings for the function’s free variables. See below for information on the cell_contents attribute.

avg = make_average()
print(avg.__closure__)
print(avg.__closure__[0].cell_contents)
print(avg.__code__.co_varnames,avg.__code__.co_freevars)
print(avg(10))
print(avg(11))
print(avg(12))
print(avg.__closure__)
print(avg.__closure__[0].cell_contents)
print(avg.__code__.co_varnames,avg.__code__.co_freevars)


# co_varnames	tuple of names of arguments and local variables  co_freevars	tuple of names of free variables (referenced via a function’s closure)
#其实，闭包指延伸了作用域的函数，其中包含函数定义体中引用、但是不在定义体中定义的非全局变量。函数是不是匿名的没有关系，关键是它能访问定义体之外定义的非全局变量
#意思就是闭包中的内部函数对象保存着自己的局部变量和自由变量。自由变量对于外部函数来说是一个局部变量。保存在对象的__closuere__属性中。对象的__closure__是一个列表
#p317很精彩  数字字符创或者元组等不可变对象的+=会隐式的创建局部变量。只能读取，不能更新，而listdict等可变对象则不会。Python 3 引入了 nonlocal 声明。它的作用是把变量标记为自由变量，
#即使在函数中为变量赋予新值了，也会变成自由变量。如果为 nonlocal 声明的变量赋予新值，闭包中保存的绑定会更新。

def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count,total  #没有这一行会吧count和total变成局部变量local variable 'count' referenced before assignment
        count += 1
        total += new_value
        return total/count

    return averager

avg=make_averager()
print(avg.__closure__)
print(avg.__closure__[0].cell_contents)
print(avg.__code__.co_varnames,avg.__code__.co_freevars)
print(len(avg.__closure__))
print(avg(10))
print(avg(11))
print(avg(12))
print(avg.__closure__)
print(avg.__closure__[0].cell_contents)
print(avg.__code__.co_varnames,avg.__code__.co_freevars)
print(len(avg.__closure__))



装饰器最好通过实现 __call__ 方法的类实现

函数装饰器在导入模块时立即执行，而被装饰的
函数只在明确调用时运行
装饰器函数与被装饰的函数在同一个模块中定义。实际情况是，装
饰器通常在一个模块中定义，然后应用到其他模块中的函数上。


#参数化装饰器只有在装饰器是函数的时候使用
def Func1(arg_a,arg_b,...):
    pass

def Func2(arg_A,arg_B,...):
    pass

@Func2(arg_A,arg_B,...)
@Func1(arg_a,arg_b,...)
def Func(arg_x,arg_y,...):
    pass

yinyong = Func2(arg_A,arg_B,...)(Func1(arg_a,arg_b,...)(Func))


因为一般的装饰器是
@decorator()
def func(a, b):
    pass

<=> func = decorator(func)(a,b)
带有参数的装饰器：
@decorator(x, y, z)
def func(a, b):
    pass

def func(a, b):
    pass
func = decorator(x, y, z)(func)

而decorator的样子是：

def decorator(x,y,z):
    def outer(func):
        def inner(*args,**kwargs):
            ...
        return inner
    return outer
所以func = decorator(x, y, z)(func)返回的是内层inner函数


返回的可能是某个引用。比如闭包中的函数体对于外部来说就是内部函数。外部函数返回内部函数对象。装饰之后返回的是这个内部函数对象的引用，然后functools.wraps 装饰器把相关的属性拷贝到内部函数对象的__doc__和__name__因为这两个属性是可写的
https://docs.python.org/3/reference/datamodel.html?highlight=closure


# 类装饰器没有参数
class A:
  pass
A = foo(bar(A))


@foo
@bar
class A:
  pass

#类装饰器装饰函数要有call方法

class A:
    def __init__(self,func):
        self._func=func
    def __call__(self,*args,**kwargs):
        self._func(*args,**kwargs)

@A
def func(*args,**kwargs):
    ...

result = func(*args,**kwargs)  <==> A(func)(*args,**kwargs)

'''


# 抽象基类  元类
'''
元类是创建类的类。这个概念已经超过c++了。没卵用。python有很多元类。包括type abc.ABCMeta(从type继承过来创建类的能力)。没卵用


抽象基类其实就相当于c++中的抽象类。abstractmethod方法就相当于纯虚函数。为了抽象和设计的目的而建立的
抽象类不能被实例化。但是纯虚函数的实现可以由子类全部实现，记得是必须全部实现。
如果子没有重新定义纯虚函数，而子类只是继承基类的纯虚函数，则这个派生类仍然还是一个抽象类。
abstractmethod() 应该放在最里层

python有很多抽象基类。collections.abc 模块中定义了 16 个抽象基类。
abc.ABC 类。每个抽象基类都依赖这个类。
继承abc.ABC这个就是创建抽象基类。跟ABCMeta关系如下
class ABC(metaclass=ABCMeta):
    """Helper class that provides a standard way to create an ABC using
    inheritance.
    """
    pass
'''





'''
引用 弱引用


del 语句删除名称，而不是对象。del 命令可能会导致对象被当作垃圾
回收，但是仅当删除的变量保存的是对象的最后一个引用，或者无法得
到对象时。 重新绑定也可能会导致对象的引用数量归零，导致对象被
销毁。
a=(1,2,3)
b=(4,5)
print(id(a))
print(id(b))
a=a+b
print(id(a))

class K:
    def haha(self):
        self = None

a = K()
a.haha()
print(a) # a is still an instance

self=None应该是清空对自身(self)的引用。保留最后本身(self)-也就是引用计数为1

WeakValueDictionary 类实现的是一种可变映射，里面的值是对象的
弱引用。被引用的对象在程序中的其他地方被当作垃圾回收后，对应的
键会自动从 WeakValueDictionary 中删除。WeakKeyDictionary也是可变映射。里面的键是对象的弱引用
被引用的对象在程序中其他地方被当做辣鸡回收后。对应的值会自动从WeakKeyDictionary删除


弱引用对象不会增加对象的引用数量。引用的目标对象称为所指对象
（referent）。因此我们说，弱引用不会妨碍所指对象被当作垃圾回收。





创建一个弱引用对象，object是被引用的对象
弱引用对象是可调用的对象，返回的是被引用的对象；如果所指对象不存在了，返回 None ：  a = weakref.ref(object[, callback]) a()返回的是被引用的对象

class weakref.ref(object[, callback])
Return a weak reference to object. The original object can be retrieved by calling the reference object if the referent is still alive; if the referent is no longer alive,
calling the reference object will cause None to be returned.

If callback is provided and not None, and the returned weakref object is still alive, the callback will be
 called when the object is about to be finalized; the weak reference object will be passed as the only parameter to the callback; the referent will no longer be available.
 （当被引用对象即将被删除时，会调用改函数）

It is allowable for many weak references to be constructed for the same object. Callbacks registered for each weak reference will be called from the most recently registered
callback to the oldest registered callback.

Exceptions raised by the callback will be noted on the standard error output, but cannot be propagated; they are handled in exactly the same way as exceptions raised from an
 object’s __del__() method.

Weak references are hashable if the object is hashable. They will maintain their hash value even after the object was deleted. If hash() is called the first time only after
 the object was deleted, the call will raise TypeError.

Weak references support tests for equality, but not ordering. If the referents are still alive, two references have the same equality relationship as their referents (regardles
s of the callback). If either referent has been deleted, the references are equal only if the reference objects are the same object.

'''










'''
concurrent---
            | multiprocessing
            | threading
            | queue
            | sche
            | subprocess
            | concurrent.futures

socket_select------
            |socket
            |socketserver
            |selectors
# be patience..  day by day ... finally will be strongest

'''

'''

The concurrent package,Currently, there is only one module in this package:concurrent.futures

Lib/concurrent/futures/thread.py and Lib/concurrent/futures/process.py

并发是指一次处理多件事。---协程，多线程
并行是指一次做多件事。 ---多进程 cpu核数相关


抨击线程的往往是系统程序员，他们考虑的使用场景对一般的应用
程序员来说，也许一生都不会遇到……应用程序员遇到的使用场
景，99% 的情况下只需知道如何派生一堆独立的线程，然后用队列
收集结果--线程之间最好的交流方式是队列

标准库中所有执行阻塞型 I/O 操作的函数，在等待操作系统返回
结果时都会释放 GIL。这意味着在 Python 语言这个层次上可以使用多线
程，而 I/O 密集型 Python 程序能从中受益：一个 Python 线程等待网络响
应时，阻塞型 I/O 函数会释放 GIL，再运行一个线程----即标准库中每个使用 C 语言编写的 I/O 函数都会释放 GIL，因
此，当某个线程在等待 I/O 时， Python 调度程序会切换到另一个线程。
因此 David Beazley 才说：“Python 线程毫无作用。　。time.sleep() 函数也会释放 GIL。因此，尽管有
GIL，Python 线程还是能在 I/O 密集型应用中发挥作用。


concurrent中thread.py用到了threading。process.py用到了multiprocessing.py  multiprocessing用到了threading
# 粗略看了下multiprocessing。提供的贡共享方式。我觉得也不实用。也不安全。要安全也麻烦要锁啥的。不如直接队列。然后没了。池子比较实用
# get_context pool queue process就没了

对 CPU 密集型工作来说，要启动多个进程，规避 GIL。创建多个进程最
简单的方式是，使用 futures.ProcessPoolExecutor。对于IO密集型来说。要启动多个线程。就用future.ThreadPoolExecutor就ok。对于要进程之间共享数据的话就multiprocessing
而且是用queue。别搞啥其他花里胡哨。同时queue里的数据对于处理函数来说要可picklable
'''



# iter iterable iterator generator yield yield from contextmanage 协程couroutine  asyncio



# 读tornado源码的时候需要关注它的代码结构--为了观察import
