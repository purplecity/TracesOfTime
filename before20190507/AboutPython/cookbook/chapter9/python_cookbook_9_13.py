# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/18 3:20 PM                               
#  Author           purplecity                                       
#  Name             python_cookbook_9_13.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

#元类控制实例的创建  --->单例等会比较简洁

#诶呀都没讲本质。看来有事没事多去看官方文档会比较好

'''不允许实例化
class NoInstances(type):  #type....
    def __call__(self, *args, **kwargs):
        raise TypeError("can't instantiate directly")

class Spam(metaclass=NoInstances):
    @staticmethod
    def grok(x):
        print('Spam.grok')
'''




'''
元类，__new__ __init__ __call__  type object  初步总结：先感叹一下还是python官方文档靠谱


1 首先type和object是鸡生蛋蛋生鸡的关系 不用纠结。但是具体可以用那张图表示   https://blog.csdn.net/f1ngf1ngy1ng/article/details/80361196
所有类的最祖宗基类是object。所有类都是type类型。所有类包括type自身是type类的实例。

要创建一个class对象，type()函数依次传入3个参数：

class的名称；
继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；
class的方法名称与函数绑定，这里我们把函数fn绑定到方法名func上。
通过type()函数创建的类和直接写class是完全一样的，因为Python解释器遇到class定义时，仅仅是扫描一下class定义的语法，然后调用type()函数创建出class。


2  __new__ __init__ __call__ 在type和object的不同。这里的object指祖宗。任何类都有object的__new__方法

type.__new__就是创建一个未被初始化的类
type.__init__就是初始化类
object__new__就是创建一个未被初始化的实例
object.__init__就是初始化实例

上面的new都有返回值。但是参数有区别。一个cls省略。一个要写


type.__new__(cls,name,bases,attrs)

cls: 将要创建的类，这里cls指向的是class。实际用的时候不用赋值跟self一样
name: 类的名字，也就是我们通常用类名.__name__获取的。 所以写class xxx的时候就是type.__new__ 并且把xxx作为类名
bases: 基类
attrs: 属性的dict。dict的内容可以是变量(类属性），也可以是函数（类方法）。


object.__new__(cls,*args,**kwargs) 
cls:指的是要实例化的类。哪个类invoke就是哪个类


__call__方法先看官方定义:
对象通过提供__call__(slef, *args ,**kwargs)方法可以模拟函数的行为，如果一个对象x提供了该方法，就可以像函数一样使用它，也就是说x(arg1, arg2...) 等同于调用x.__call__(self, arg1, arg2) 。
object.__call__(self[, args...])
Called when the instance is “called” as a function; if this method is defined, x(arg1, arg2, ...) is a shorthand for x.__call__(arg1, arg2, ...).

本来是__call__跟__new__ 和__init__是半毛钱关系没有的。但是应该是内部设置成(反正我没看见，python学习手册是这么说。而且应该是子元类的转换)    
type.__call__(classname, superclasses, attributedict))   会转化为
type.__new__(typeclass, classname, superclasses, attributedict)
type.__init__(class, classname, superclasses, attributedict)

原因呢很简单。下面的例子Date=type("Date",(),{}） 其实就是创建了一个类。首先ype("Date",(),{}）既然是创建了类。然后也就是说x(arg1, arg2...) 等同于调用x.__call__(self, arg1...)这个说法
得出结论type的默认call方法是调用了__new__和__init__方法的 。但是又跟最后实际打印有冲突这说法。确认是创建先call然后new和init的。但是应该是调用子元类的new和init。不然跟那个单例例子说不通
https://www.jianshu.com/p/ad976b494486  type_call -> tp_new ->tp_init

object.__new__ 和object.__init__。只是也是先__new__ 再__init__.  print(dir(object))  object原始类确实是没有__call__的
class A(object):
    def __init__(self,*args, **kwargs):
        print "init %s" %self.__class__
    def __new__(cls,*args, **kwargs):
        print "new %s" %cls
        return object.__new__(cls, *args, **kwargs)

a = A()
new <class '__main__.A'>
init <class '__main__.A'>


class B(object)
    def __init__(self):
        print('a')
    
    def __call__(self):
        print('call')
        
x=B()
x()  #call

但是不管是type可以通过继承可以改变call不去调用__new__和__init__。 





举例：
class Date:pass
        
对于object的调用d = Date.__new__(Date) print(d) 只不过没属性。要自己添加
实际Date的create是调用  Date=type("Date",(),{}） 只不过没属性，要自己添加
还可以直接  Date=type("xxx",(),{}） 生成一个类 print('Date')然后出现xxx class



重要！！！ 虽然说。可以type对应的类的创建   或者   object对应的实例的创建   都可以先new再init。  但是我看网上的例子或者都是可以直接init跳过new。也就是说自定义的元类也可以不写new方法直接写init方法



Date=type("xxx",(),{})
print(Date)  #<class '__main__.xxx'>
'''
'''
class SingletonType(type):

    def __new__(cls, name, bases, dct):  # cls为元类Meta
        print('yuanlei new')
        print(cls)
        return type.__new__(cls, name, bases, dct)

    def __init__(cls, *args, **kwargs):
        print('元类__init__')
        print(cls)
        super(SingletonType, cls).__init__(*args, **kwargs)

    def __call__(cls, *args, **kwargs):
        print('元类__call__')
        obj = cls.__new__(cls, *args, **kwargs)
        cls.__init__(obj, *args, **kwargs)  # Foo.__init__(obj)
        return obj


class Foo(metaclass=SingletonType):
    #pass  #这样的话Foo不能实例化因为没有new

    def __init__(self, name):
        print("Foo __init__")
        self.name = name

    
    def __new__(cls, *args, **kwargs):
        print('Foo __new__')
        return object.__new__(cls)

    def __call__(self,*args,**kwargs):
        print('foo __call__')
        return object.__call__(self)


yuanlei new
<class '__main__.SingletonType'>
元类__init__
<class '__main__.Foo'>
# 会自动打印。还没执行下面的代码就会自动打印!!! 在class Foo定义就执行了这是关键
'''



#obj = Foo('name')
#原因在这里Foo是SingletonType的一个实例。所以Foo('name')或者Foo()都会执行SingletonType的call方法  然后call方法调用Foo的new和init形成实例。跟什么拦截半毛钱关系没有
#print(obj)


#  最后如果SingletonType没有__call__ __new__ __init__就去找父类的就这么简单



class Singleton(type):
    def __init__(self,*args,**kwargs):
        self.__instance=None
        print(self)
        print(1)  #<class '__main__.Spam'>
        print(Singleton.__mro__)  #(<class '__main__.Singleton'>, <class 'type'>, <class 'object'>)
        super().__init__(*args,**kwargs)  #super肯定是mro的type

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            print(self)  #<class '__main__.Spam'>
            self.__instance=super().__call__(*args,**kwargs)   # 但是一个产生类。一个产生实例。莫非。是super的继续寻找？？？？yes！！ super每调用一次就mro列表往后一次

            print(self.__instance)  #__main__.Spam object at 0x1018c7518>
            return self.__instance
        else:
            return self.__instance

class Spam(metaclass=Singleton):
    def __init__(self):
        print('creating spam')

print(dir(Spam))
print(Spam.__dict__)   #'_Singleton__instance': None

a=Spam()

print(dir(Spam))
print(Spam.__dict__)  #_Singleton__instance': <__main__.Spam object at 0x10efdf588>  #自己的类中有一个自己的对象我日呢


'''
#先打印1
print(Spam.__mro__)
print(Singleton.__mro__)
print(Spam.__dict__)
print(dir(Spam))
a=Spam()
print(Spam.__dict__)  #_Singleton__instance有变化
b=Spam()
#_Singleton__instance
'''
'''
<class '__main__.Spam'>
1
(<class '__main__.Spam'>, <class 'object'>)
(<class '__main__.Singleton'>, <class 'type'>, <class 'object'>)
creating spam
<__main__.Spam object at 0x10754b550>


def super(cls, inst):
    mro = inst.__class__.mro()
    return mro[mro.index(cls) + 1]
其中，cls 代表类，inst 代表实例，上面的代码做了两件事：

获取 inst 的 MRO 列表
查找 cls 在当前 MRO 列表中的 index, 并返回它的下一个类，即 mro[index + 1]
当你使用 super(cls, inst) 时，Python 会在 inst 的 MRO 列表上搜索 cls 的下一个类。

感觉inst也可以是class暂时结合下面这样理解吧。就是返回inst 的mro列表的cls的下一个类。

综合        super(type, obj) -> bound super object; requires isinstance(obj, type)
        super(type, type2) -> bound super object; requires issubclass(type2, type)
        
        
在类中如果没有参数就是指类名的mro列表的下一个类

'''

#关于super参考8.7 8.8

'''
1 在出现class Spam的时候就已经开始操作了.
Spam=Singleton("SPam",(),{}) 然后==》 会调用Singleton的__call__方法。显然这就不会滴啊用Singleton的方法了跟打印1矛盾。如果是type("Spam",(),{}）也矛盾

元类的处理过程。暂时相信这篇文章的说法 https://www.cnblogs.com/huchong/p/8260151.html

元类处理过程：定义一个类时，使用声明或者默认的元类对该类进行创建，对元类求type运算，得到父元类（该类声明的元类的父元类），调用父元类的__call__函数，在父元类的__call__函数中, 调用该类声明的元类的__new__函数来创建对象（该函数需要返回一个对象（指类）实例），然后再调用该元类的__init__初始化该对象（此处对象是指类，因为是元类创建的对象），最终返回该类
那么

 <class 'object'>)    self.__instance=super().__call__(*args,**kwargs) 如果这里也是会父类的call函数会调用子类的init和new的话就ok了。看来产生实例的确是这样
'''


# aaa 是真的服气。
# 1元类的call怎么调用。难道真如所说？https://www.cnblogs.com/huchong/p/8260151.html
# 2  self.__instance=super().__call__(*args,**kwargs) 如果是super往mro后搜索，1为啥不管是为啥还有super会有call方法2init的返回是一个类这里为啥返回一个实例3返回实例居然还打印了print('creating spam')？？？ super跟call啥关系？



#不纠结了。super跟元类结合没搞清楚。 单纯的继承super倒是没有问题就是9-17的我觉得是有问题的。实例化的


print("^"*20)


