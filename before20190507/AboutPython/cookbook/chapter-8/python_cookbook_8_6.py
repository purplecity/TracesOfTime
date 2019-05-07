# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
#  Time             2018/9/7 11:24 AM                               
#  Author           purplecity                                       
#  Name             python_cookbook_8_6.py                                    
#  Description                                                    
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# 创建可管理的逻辑。property。 印象中property是描述器的一个特殊例子
'''


class property(object):
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

    Decorators make defining new properties or modifying existing ones easy:

    class C(object):
        @property
        def x(self):
            "I am the 'x' property."
            return self._x
        @x.setter
        def x(self, value):
            self._x = value
        @x.deleter
        def x(self):
            del self._x
    """
    def deleter(self, *args, **kwargs): # real signature unknown
        """ Descriptor to change the deleter on a property. """
        pass

    def getter(self, *args, **kwargs): # real signature unknown
        """ Descriptor to change the getter on a property. """
        pass

    def setter(self, *args, **kwargs): # real signature unknown
        """ Descriptor to change the setter on a property. """
        pass

    def __delete__(self, *args, **kwargs): # real signature unknown
        """ Delete an attribute of instance. """
        pass

    def __getattribute__(self, *args, **kwargs): # real signature unknown
        """ Return getattr(self, name). """
        pass

    def __get__(self, *args, **kwargs): # real signature unknown
        """ Return an attribute of instance, which is of type owner. """
        pass

    def __init__(self, fget=None, fset=None, fdel=None, doc=None): # known special case of property.__init__
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

        Decorators make defining new properties or modifying existing ones easy:

        class C(object):
            @property
            def x(self):
                "I am the 'x' property."
                return self._x
            @x.setter
            def x(self, value):
                self._x = value
            @x.deleter
            def x(self):
                del self._x

        # (copied from class doc)
        """
        pass

    @staticmethod # known case of __new__
    def __new__(*args, **kwargs): # real signature unknown
        """ Create and return a new object.  See help(type) for accurate signature. """
        pass

    def __set__(self, *args, **kwargs): # real signature unknown
        """ Set an attribute of instance to value. """
        pass

    fdel = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    fget = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    fset = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default

    __isabstractmethod__ = property(lambda self: object(), lambda self, v: None, lambda self: None)  # default
'''

class Person:
    def __init__(self, first_name):
        self.set_first_name(first_name)
        #self._first_name=first_name  #硬是要这样才报有这个属性
    # Getter function
    def get_first_name(self):
        return self._first_name

    # Setter function
    def set_first_name(self, value):
        if not isinstance(value, str):
            raise TypeError('Expected a string')
        self._first_name = value

    # Deleter function (optional)
    def del_first_name(self):
        raise AttributeError("Can't delete attribute")

    # Make a property from existing get/set methods
    name = property(get_first_name, set_first_name, del_first_name)

p=Person('hehe')
print(p._first_name)  #AttributeError: 'Person' object has no attribute '_fisrt_name'  ?????
print(p.name)
print(p.get_first_name())
p.set_first_name('yes')
print(p.get_first_name(),p.name)
# hehe
# hehe
# yes yes


# 1 不要采用装饰器修饰的方式，就采用name=property(...)这样的方法。.name就会触发fget方法. =就会触发fset方法
# 2.  import math
# class Circle:
#     def __init__(self, radius):
#         self.radius = radius
#
#     @property
#     def area(self):
#         return math.pi * self.radius ** 2
#
#     @property
#     def diameter(self):
#         return self.radius * 2
#
#     @property
#     def perimeter(self):
#         return 2 * math.pi * self.radius



# 描述符合property官方文档阅读：

class RevealAccess(object):
    """A data descriptor that sets and returns values
       normally and prints a message logging their access.
    """

    def __init__(self, initval=None, name='var'):
        self.val = initval
        self.name = name

    def __get__(self, obj, objtype):
        print('Retrieving', self.name)
        return self.val

    def __set__(self, obj, val):
        print('Updating', self.name)
        self.val = val

class MyClass(object):
    x=RevealAccess(10,'var "c"')
    y=5

m=MyClass()
print(m.x)
m.x=20
print(m.x)
print(m.y)

'''
按照involing Descriptors中的方法，b.x的转换是
if b是个objects type(b).__dict__['x'].__get__(b,type(b))
if b是个classes b.__dict__['x'].__get__(None,b)
#总结其实就是去描述符类中的get set方法。自动触发而已。
这里m是classes实例。有x。然后调用x的__get__方法  __get__中self是x本身，obj是None，objetype是b也就是m


property是一个描述符
class Property(object):
    "Emulate PyProperty_Type() in Objects/descrobject.c"

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("unreadable attribute")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("can't set attribute")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError("can't delete attribute")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

'''
#over
